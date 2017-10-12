#import the necessary packages
import cv2
import numpy as np
import sys

#'optional' argument is required for trackbar creation parameters
def nothing(arg):
    pass

#Capture video from the stream
frame = cv2.imread(sys.argv[1])
cv2.namedWindow('Colorbars', cv2.WINDOW_NORMAL) #Create a window named 'Colorbars'

#assign strings for ease of coding
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'
wnd = 'Colorbars'
#Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd,0,179,nothing)
cv2.createTrackbar(hh, wnd,0,179,nothing)
cv2.createTrackbar(sl, wnd,0,255,nothing)
cv2.createTrackbar(sh, wnd,0,255,nothing)
cv2.createTrackbar(vl, wnd,0,255,nothing)
cv2.createTrackbar(vh, wnd,0,255,nothing)
cv2.createTrackbar("sobel", wnd, 0, 255, nothing)

# for black
# cv2.setTrackbarPos(hl, wnd,0)
# cv2.setTrackbarPos(hh, wnd,179)
# cv2.setTrackbarPos(sl, wnd,0)
# cv2.setTrackbarPos(sh, wnd,255)
# cv2.setTrackbarPos(vl, wnd,0)
# cv2.setTrackbarPos(vh, wnd,30)


# for blue
# cv2.setTrackbarPos(hl, wnd,81)
# cv2.setTrackbarPos(hh, wnd,130)
# cv2.setTrackbarPos(sl, wnd,50)
# cv2.setTrackbarPos(sh, wnd,255)
# cv2.setTrackbarPos(vl, wnd,30)
# cv2.setTrackbarPos(vh, wnd,255)

# for orange
cv2.setTrackbarPos(hl, wnd,0)
cv2.setTrackbarPos(hh, wnd,177)
cv2.setTrackbarPos(sl, wnd,87)
cv2.setTrackbarPos(sh, wnd,183)
cv2.setTrackbarPos(vl, wnd,96)
cv2.setTrackbarPos(vh, wnd,107)


# http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
# cap = cv2.Vide oCapture(0)

#begin our 'infinite' while loop
while(1):

    frame = cv2.imread(sys.argv[1])
    # ret, frame = cap.read()

    #it is common to apply a blur to the frame
    res = cv2.GaussianBlur(frame,(7,7),0)
    res = cv2.GaussianBlur(res, (7,7), 0)
    res = cv2.GaussianBlur(res, (7,7), 0)
    res = cv2.GaussianBlur(res, (7,7), 0)
    # res = cv2.GaussianBlur(res, (7,7), 0)
    # res = cv2.GaussianBlur(res, (7,7), 0)
    sobelx8u = cv2.Sobel(frame, cv2.CV_8U,1,0,ksize=5)

    sobelx64f = cv2.Sobel(frame, cv2.CV_64F, 1,0,ksize=5)
    abs_sobel64f = np.absolute(sobelx64f)
    sobel_8u = np.uint8(abs_sobel64f)

    laplacian = cv2.Laplacian(res, cv2.CV_64F)


    #convert from a BGR stream to an HSV stream
    hsv=cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

    #read trackbar positions for each trackbar
    hul=cv2.getTrackbarPos(hl, wnd)
    huh=cv2.getTrackbarPos(hh, wnd)
    sal=cv2.getTrackbarPos(sl, wnd)
    sah=cv2.getTrackbarPos(sh, wnd)
    val=cv2.getTrackbarPos(vl, wnd)
    vah=cv2.getTrackbarPos(vh, wnd)
    sobel_min = cv2.getTrackbarPos("sobel", wnd)

    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    #create a mask for that range
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    inverse_mask = cv2.bitwise_not(mask)

    sobel_mask = cv2.inRange(sobel_8u, sobel_min, 255)


    white_points = cv2.findNonZero(mask)

    if white_points is not None:
        x,y,w,h = cv2.boundingRect(white_points)
        rect = cv2.minAreaRect(white_points)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        (x_c,y_c),radius = cv2.minEnclosingCircle(white_points)
        center = (int(x_c),int(y_c))
        radius = int(radius)
        cv2.circle(res,center,radius,(0,255,0),5)
        cv2.drawContours(res,[box],0,(0,0,255),2)
        cv2.rectangle(res,(x,y),(x+w,y+h),(255,255,255),5)
        # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),5)

    # res2, contours, hierarchy = cv2.findContours()

    #res = cv2.bitwise_and(frame,frame, mask =mask)

    #cv2.imshow(wnd, res)

    #res[mask == 255] = [0, 255, 0]
    #sobel_8u = cv2.resize(sobel_8u, (600, 600))
    # laplacian = cv2.resize(laplacian, (600, 600))
    sobel_mask = cv2.resize(sobel_mask, (600, 600))
    cv2.imshow('sobel', sobel_mask)

    cv2.imshow(wnd, res)
    cv2.resizeWindow(wnd, 600, 600)

    mask = cv2.resize(mask, (600, 600))
    cv2.imshow('mask', mask)

    inverse_mask = cv2.resize(inverse_mask, (600, 600))
    cv2.imshow('inverse', inverse_mask)

    k = cv2.waitKey(5)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
