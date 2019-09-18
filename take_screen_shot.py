import cv2 
import os
import numpy as np

cap = cv2.VideoCapture('/dev/video2')
camera_freq = cap.get(cv2.CAP_PROP_FPS)
img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
img_center = (img_width/2, img_height/2)		

lower_red = np.array([15, 50, 230])
upper_red = np.array([40, 155, 255])

#cv2.createTrackbar()

while (True):

	ret, frame = cap.read()
	#convert numpy matrix to represent HSV matrix
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	#make a mask that has low red and upper red hue bounds
	mask = cv2.inRange(hsv, lower_red, upper_red)

	#apply mask to our image
	res = cv2.bitwise_and(hsv, hsv, mask = mask)
	#split up resultant 3 channel image
	[h , s, v] = cv2.split(res)
	#combine to get single channel gray scale
	thresh = cv2.bitwise_or(s, v)
	#binary threshold the image
	ret,thresh = cv2.threshold(thresh, 127, 255, 0)
	# print(thresh.shape)
	#find the edges of the binary image
	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

	frame = cv2.GaussianBlur(frame, (5,5), 0)
	# print(frame.shape)
	erosion_size = 5
	erosion_type = cv2.MORPH_ELLIPSE 
	element = cv2.getStructuringElement(erosion_type, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
	frame = cv2.erode(frame, element)
	# print(frame.shape)
	frame = cv2.drawContours(frame, contours, -1, color = (255,0,0), thickness = 3)
	# print(frame.shape)
	rows = frame.shape[0]
	circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, rows/8, param1 = 100, param2=30, minRadius = 1, maxRadius = 30)

	if circles is not None:
		circles = np.unint16(np.around(circles))
		for i in circles[0,:]:
			print("drawing circles")
			center = (i[0], i[1])
			cv2.circle(frame, center, 1, (0, 100, 100), 3)
			radius = i[2]
			cv2.circle(frame, center, radius, (255,0,255), 3)


	cv2.imshow('frame', frame)

	key = cv2.waitKey(1)
	if key & 0xFF == ord('q'):
		break
	elif key & 0xFF == ord('s'):
		filename = '{}.png'.format(len(os.listdir('pictures')))
		cv2.imwrite('pictures/{}'.format(filename), frame)


cap.release()
cv2.destroyAllWindows()

