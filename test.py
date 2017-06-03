#!/usr/bin/env python

import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

def is_contour_bad(c):
	area = cv2.contourArea(c)
	
	if area < 100:
		return True

	#print area

	r = cv2.boundingRect(c)
	#print r
	w = r[2]
	h = r[3]

	#print 'box width' + str(w)
	if w > 300:

		return True

	return False

def treshold(src):
	rows = src.shape[0]
	cols = src.shape[1]

	for x in range(0, cols - 1):
		for y in range(0, rows -1):
			print src[x,y]
			break
		break

img = cv2.imread(sys.argv[1])
cv2.imshow('preview', img)

# inv = cv2.bitwise_not (img);
# cv2.imshow('inverted inv', inv)
# thresh = 250
# maxValue = 255
# th, dst = cv2.threshold(inv, thresh, maxValue, cv2.THRESH_TOZERO_INV);
# img = cv2.bitwise_not (dst);



# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_black = np.array([0,0,0])
upper_black = np.array([360,100,50])

# Threshold the HSV image to get only black colors
blackOnly = cv2.inRange(hsv, lower_black, upper_black)
cv2.imshow('blackOnly', blackOnly)
#blackOnly = cv2.bitwise_not(blackOnly)


#zeros = np.zeros((blackOnly.shape[0],blackOnly.shape[1]),'uint8')
#merged_green = np.dstack((zeros,blackOnly,zeros))
#cv2.imshow('merged green', merged_green)
#img = cv2.bitwise_and(img,img,mask=merged_green)


img[blackOnly == 255] = [0, 255, 0]
cv2.imshow('masked green', img)





# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
# params.minThreshold = 10;
# params.maxThreshold = 200;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 100
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1
 
# Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87
 
# Filter by Inertia
# params.filterByInertia = True
# params.minInertiaRatio = 0.01
 
# Create a detector with the parameters
ver = (cv2.__version__).split('.')
detector = None
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else : 
    detector = cv2.SimpleBlobDetector_create(params)

 # Detect blobs.
keypoints = detector.detect(img)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)







# Convert BGR to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

# Threshold the HSV image to get only blue colors
blueOnly = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow('blueonlye', blueOnly)
blueOnly = cv2.bitwise_not(blueOnly)

img = cv2.bitwise_and(img,img, mask= blueOnly)

cv2.imshow('masked', img)

#blueOnly = cv2.cvtColor(blueOnly, cv2.COLOR_GRAY2BGR)
#img = (img - blueOnly)

channels = cv2.split(img)

green = channels[1]
blue = channels[0]

#cv2.imshow('blue', blue)
#cv2.imshow('green', green)

new = 2*blue - green

cv2.imshow('new', new)

























# cv2.imshow(' new', new)
# new = cv2.bitwise_not (new);
# cv2.imshow('inverted new', new)
# thresh = 250
# maxValue = 255
# th, dst = cv2.threshold(new, thresh, maxValue, cv2.THRESH_TOZERO_INV);
# new = cv2.bitwise_not (dst);

# cv2.imshow('new after removing black', new)

#element = cv2.getStructuringElement(cv2.MORPH_CROSS, (2,2))
#eroded = cv2.erode(new, element, iterations = 1)




# Basic threshold example
thresh = 180
maxValue = 255
th, dst = cv2.threshold(new, thresh, maxValue, cv2.THRESH_BINARY);
cv2.imshow("thresh", dst)

(cnts, _) = cv2.findContours(dst.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#im2, cnts, hierarchy = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mask = np.zeros(img.shape[:2], dtype="uint8") * 255

cv2.imshow('mask before', mask)
 
# loop over the contours
for c in cnts:
	# if the contour is bad, draw it on the mask
	if is_contour_bad(c):
		cv2.drawContours(dst, [c], -1, 255, -1)

#cv2.imshow('mask', mask)

#mask = cv2.bitwise_not (mask);

#cv2.imshow('inverted mask', mask)

#final = cv2.bitwise_and(dst, dst, mask=mask)


cv2.imshow('final', dst)

dst = cv2.bitwise_not (dst);




minLineLength = 10
maxLineGap = 20 # 10
lines = cv2.HoughLinesP(dst,1,np.pi/180, 35 ,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


cv2.imshow('final final', img)  

cv2.waitKey(0)




