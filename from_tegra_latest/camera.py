
import cv2
import numpy as np
import sys

# Taken with two blocks in between for meters


cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

ret, frame = cap.read()
ret2, frame2 = cap2.read()

cv2.imwrite( "./left.jpg", frame);
cv2.imwrite( "./right.jpg", frame2);

