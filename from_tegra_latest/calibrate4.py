import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_GRAYSCALE)
height,width = img.shape
print width
print height

pts2 = np.float32([[0,0],[0,height],[width,height]])
pts1 = np.float32([[160,36],[60,153],[296,204]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(width,height))

cv2.imshow('Input',img)
cv2.imshow('Output',dst)

cv2.waitKey(0)


