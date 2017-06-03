#import the necessary packages
import cv2
import numpy as np
import sys

#'optional' argument is required for trackbar creation parameters
def nothing(arg):
    pass
 
#Capture video from the stream
#frame = cv2.imread(sys.argv[1])
cv2.namedWindow('Colorbars') #Create a window named 'Colorbars'
 
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

# for black
# cv2.setTrackbarPos(hl, wnd,0)
# cv2.setTrackbarPos(hh, wnd,179)
# cv2.setTrackbarPos(sl, wnd,0)
# cv2.setTrackbarPos(sh, wnd,255)
# cv2.setTrackbarPos(vl, wnd,0)
# cv2.setTrackbarPos(vh, wnd,30)


# for blue
cv2.setTrackbarPos(hl, wnd,81)
cv2.setTrackbarPos(hh, wnd,130)
cv2.setTrackbarPos(sl, wnd,50)
cv2.setTrackbarPos(sh, wnd,255)
cv2.setTrackbarPos(vl, wnd,50)
cv2.setTrackbarPos(vh, wnd,255)

# for orange
# cv2.setTrackbarPos(hl, wnd,0)
# cv2.setTrackbarPos(hh, wnd,26)
# cv2.setTrackbarPos(sl, wnd,155)
# cv2.setTrackbarPos(sh, wnd,255)
# cv2.setTrackbarPos(vl, wnd,24)
# cv2.setTrackbarPos(vh, wnd,255)


cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

#begin our 'infinite' while loop
while(1):
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()

    #it is common to apply a blur to the frame
    res = cv2.GaussianBlur(frame,(7,7),0)
    res2 = cv2.GaussianBlur(frame2,(7,7),0)
    
 
    #convert from a BGR stream to an HSV stream
    hsv=cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    hsv2=cv2.cvtColor(res2, cv2.COLOR_BGR2HSV)

    #read trackbar positions for each trackbar
    hul=cv2.getTrackbarPos(hl, wnd)
    huh=cv2.getTrackbarPos(hh, wnd)
    sal=cv2.getTrackbarPos(sl, wnd)
    sah=cv2.getTrackbarPos(sh, wnd)
    val=cv2.getTrackbarPos(vl, wnd)
    vah=cv2.getTrackbarPos(vh, wnd)
 
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])
 
    #create a mask for that range
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    mask2 = cv2.inRange(hsv2,HSVLOW, HSVHIGH)

    #res = cv2.bitwise_and(frame,frame, mask =mask)
 
    #cv2.imshow(wnd, res)
    #cv2.imshow(wnd, res)

    res[mask == 255] = [0, 255, 0]
    cv2.imshow(wnd, res)

    cv2.imshow('mask', mask)
    cv2.imshow('mask2', mask2)

    

    k = cv2.waitKey(1)
    if k ==1048689:
        cv2.imwrite( "./mask1.jpg", mask);
        cv2.imwrite( "./mask2.jpg", mask2);
        break

 
cv2.destroyAllWindows()


