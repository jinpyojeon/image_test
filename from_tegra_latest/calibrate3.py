import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_GRAYSCALE)

height,width = img.shape
print width
print height

pts1 = np.float32([[160,36],[287,17],[60,153],[221,189]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])


M = cv2.getPerspectiveTransform(pts1,pts2)

# img2 = cv2.imread(sys.argv[2])
# cv2.imshow('img', img2)

dst = cv2.warpPerspective(img,M,(width,height))
#dst2 = cv2.warpPerspective(img,M,(width,height))




cv2.imshow('Input',img)
cv2.imshow('Output',dst)

# cv2.imwrite('./test.jpg',dst)

# cv2.imshow('Output2',dst2)sxd


# M2 = cv2.getPerspectiveTransform(pts2,pts1)
# dst3 = cv2.warpPerspective(dst,M2,(width,height))

# cv2.imshow('Output3',dst3)

cv2.waitKey(0)

# 2
# x: 221  y: 189
# 6
# x: 60  y: 153
# 30
# x: 160  y: 36
# 37
# x: 287  y: 17



