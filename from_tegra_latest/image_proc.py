#!/usr/bin/python

import numpy as np
import cv2
import time
import rospy
from std_msgs.msg import Int16MultiArray


def process_line(src):
	org = src.copy()

	# get size
	(height, width, _) = src.shape

	# blur image
	src = cv2.blur(src,(7,7))

	# convert BGR to HSV
	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

	# BEGIN BARREL AND SHADOW REMOVAL
	# BARRELS #####################################################
	# define range of orange color in HSV
	lower_orange = np.array([0,87,107])
	upper_orange = np.array([15,169,232])

	# extract orange colored pixels
	orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

	# find big orange contours in mask
	(cnts, _) = cv2.findContours(orange_mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	# draw box enclosing all big contours, done to enclose the white strpes in between
	min_area = 450  # anything smaller than this is removed
	min_x, min_y = width, height
	max_x = max_y = 0
	count = 0
	for c in cnts:
		# if the contour is small, color it black
		a = cv2.contourArea(c)
		if a >= min_area:
			count = count + 1
			(x,y,w,h) = cv2.boundingRect(c)
			min_x, max_x = min(x, min_x), max(x+w, max_x)
			min_y, max_y = min(y, min_y), max(y+h, max_y)
			cv2.rectangle(orange_mask, (x, y-h), (x+w, y+h+h), (255, 255, 255), -1)

	# constrain the width so that it is not too wide
	if max_x - min_x < 240 and count:
		pass
		#cv2.rectangle(orange_mask, (min_x, min_y), (max_x, max_y), (255, 255, 255), -1)

	# colora range remove patches
	l = np.array([0,40,24])
	u = np.array([34,255,255])
	patch_mask = cv2.inRange(hsv, l, u)

	cv2.imshow('patch',patch_mask)

	# SHADOW #####################################################
	# define range of black color in HSV
	lower_black = np.array([0,0,0])
	upper_black = np.array([179,255,30])

	# extract black colored pixels
	black_mask = cv2.inRange(hsv, lower_black, upper_black)


	# BLUE BARREL ################################################
	# define range of blue color in HSV
	lower_blue = np.array([81,50,30])
	upper_blue = np.array([130,255,255])

	# extract blue colored pixels
	blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

	cv2.imshow('orange_mask', orange_mask)
	cv2.imshow('black_mask', black_mask)
	cv2.imshow('blue_mask', blue_mask)

	# combine masks
	mask = cv2.bitwise_or(orange_mask, black_mask)
	mask = cv2.bitwise_or(mask, blue_mask)
	mask = cv2.bitwise_or(mask, patch_mask)
	# END BARREL AND SHADOW REMOVAL"""


	# BEGIN LINE DETECTION
	# split RGB channels
	channels = cv2.split(src)
	blue = channels[0]
	green = channels[1]


	# 2*blue - green channel works best for removing the grass
	mixed = np.subtract(np.multiply(2,blue),green)

	cv2.imshow('mixed',mixed)


	# treshold image
	thresh = 180
	maxValue = 255
	(_ , threshed) = cv2.threshold(mixed, thresh, maxValue, cv2.THRESH_BINARY);

	cv2.imshow('threshed',threshed)

	# combine with mask
	threshed[mask == 255] = [0]

	


	#cv2.imshow('mask',mask)

	cv2.imshow('masked',threshed)


	# perform hough transform
	#th_copy = cv2.bitwise_not(threshed)
	minLineLength = 35
	maxLineGap = 15
	lines = cv2.HoughLinesP(threshed,1,np.pi/180, 35,minLineLength,maxLineGap)

	if lines != None:
		for x1,y1,x2,y2 in lines[0]:
			cv2.line(org,(x1,y1),(x2,y2),(0,255,0),2)

		cv2.imshow('lines', org)

		# return array of line end points
		return lines[0]
	return []

	
def main():
	#rospy.init_node('image_proc')

	#line_pub = rospy.Publisher('PointsJ2', Int16MultiArray, queue_size=10)

	# open camera
	cap = cv2.VideoCapture(0)

	# TODO: check if camera is opened

	#rate = rospy.Rate(1)
	#while not rospy.is_shutdown():
	while True:
		print 'new frame'
		# get frame
		ret, frame = cap.read()
		# reduce size
		frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

		cv2.imshow('frame',frame)

		# get white lines
		lines = process_line(frame)
		# publish points
		#m = Int16MultiArray()
		#m.data = lines.ravel() # ravel is used to combine all rows to one (because the subscriber node expects it as such)
		#line_pub.publish(m);

		#rate.sleep()

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()

if __name__ == '__main__':
	main()
