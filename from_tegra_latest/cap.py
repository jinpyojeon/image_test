
import numpy as np
import cv2
import time

def main():
	#rospy.init_node('image_proc')

	#line_pub = rospy.Publisher('PointsJ2', Int16MultiArray, queue_size=10)

	# open camera
	cap = cv2.VideoCapture(0)

	# TODO: check if camera is opened

	#rate = rospy.Rate(1)
	#while not rospy.is_shutdown():

	count = 4000
	while True:
		count = count +1
		print 'new frame'
		# get frame
		ret, frame = cap.read()

		cv2.imshow('frame', frame)
		
		name = 'i' + str(count) + '.jpg'
		cv2.imwrite(name, frame);

		if count > 4005:
			break

		#rate.sleep()

		if cv2.waitKey(1) & 0xFF == ord('q'):
			
			break

	# When everything done, release the capture
	cap.release()

if __name__ == '__main__':
	main()