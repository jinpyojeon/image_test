#import the necessary packages
import cv2
import numpy as np
import sys


#Capture video from the stream
frame = cv2.imread(sys.argv[1],cv2.CV_LOAD_IMAGE_GRAYSCALE)
(height, width) = frame.shape

frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

cv2.imshow('frame', frame)

frame = cv2.blur(frame,(7,7))

(cnts, _) = cv2.findContours(frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

min_x, min_y = width, height
max_x = max_y = 0

count = 0

col = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

text = '1'

f = open('point_coord.txt', 'wt') 

for c in cnts:
    
    count = count + 1
    text = str(count)
    (x,y,w,h) = cv2.boundingRect(c)

    min_x, max_x = min(x, min_x), max(x+w, max_x)
    min_y, max_y = min(y, min_y), max(y+h, max_y)

    #cv2.rectangle(col, (x, y), (x+w, y+h), (0, 255, 0), 1)

    #cv2.rectangle(col, (x, y), (x+count, y+count), (0, 0, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(col, text, (x,y), font, 1,(255,255,255))
    
    # with open('point_coord.txt', 'at')  as f:
    f.write(text + '\n')
    f.write(str((x+w)/2) + '\n')
    f.write(str((y+h)/2) + '\n')

    if text == '36':
        print text
        print 'x: ' + str((x+w)/2) + '  y: ' + str((y+h)/2) 


col = cv2.resize(col,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

cv2.imshow('frame', col)

cv2.waitKey(0)
