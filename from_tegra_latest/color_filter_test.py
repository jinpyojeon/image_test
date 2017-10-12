#import the necessary packages
import cv2
import numpy as np
import sys
import shutil, os
#'optional' argument is required for trackbar creation parameters

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


# http://docs.opencv.org/3.2.0/d4/d73/tutorial_py_contours_begin.html
# cap = cv2.Vide oCapture(0)

if not os.path.isdir('./results'):
    os.mkdir('./results')

for f in os.listdir(sys.argv[1]):
    print f
    frame = cv2.imread(sys.argv[1] + '/' + f)
    if frame is None:
        continue
    height, width, _ = frame.shape

    # ret, frame = cap.read()
    print 'processsing', f
    #it is common to apply a blur to the frame
    res = cv2.GaussianBlur(frame,(9,9),0)
    # res = frame.copy()

    #convert from a BGR stream to an HSV stream
    hsv=cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

    #read trackbar positions for each trackbar
    hul = 25
    huh = 35
    sal = 90
    sah = 110
    val = 200
    vah = 255

    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    #create a mask for that range
    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)

    white_points = cv2.findNonZero(mask)

    if white_points is not None:
        x,y,w,h = cv2.boundingRect(white_points)
        # rect = cv2.minAreaRect(white_points)
        # box = cv2.cv.BoxPoints(rect)
        # ox = np.int0(box)

        #if y > (height / 2):
            # h = h + y
            # y = 0
        #else:
            # h = height - y;
        #(x_c,y_c),radius = cv2.minEnclosingCircle(white_points)
        #center = (int(x_c),int(y_c))
        #radius = int(radius)
        #cv2.circle(res,center,radius,(0,255,0),5)
        #cv2.drawContours(res,[box],0,(0,0,255),2)
        cv2.rectangle(res,(x,y),(x+w,y+h),(0,0,0),-1)
        # cv2.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),5)

    #cv2.imshow('hel', res)
    #cv2.waitKey(0)
    # res2, contours, hierarchy = cv2.findContours()

    #res = cv2.bitwise_and(frame,frame, mask =mask)

    #cv2.imshow(wnd, res)
    vis = np.concatenate((frame, res), axis=1)


    # res[mask == 255] = [0, 255, 0]
    new_image_name = f.split('.')[0] + "-filtered." + f.split('.')[1]
    cv2.imwrite('./results/' + new_image_name, vis)


cv2.destroyAllWindows()
