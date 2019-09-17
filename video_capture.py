import cv2
import numpy as np
import time
import argparse
import pdb
from pprint import pprint
#argument parsing

class Camera():
	def __init__(self):
		run_state = self.parse_args()
		self.camera_init()
		self.mask_init()


		if (run_state == 'save'):
			self.camera_loop()
		elif (run_state == 'play'):
			print("implement this feauture yo")

	def camera_init(self):
		self.cap = cv2.VideoCapture('/dev/video2')
		camera_freq = self.cap.get(cv2.CAP_PROP_FPS)
		self.img_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.img_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)		

		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.bottom_left_corner = (10, 440)
		self.font_color = (255,255,255)
		self.line_type = 2

	def mask_init(self):
		self.lower_red = np.array([20, 100, 127])
		self.upper_red = np.array([40, 255, 255])

	def parse_args(self):
		parser = argparse.ArgumentParser()
		group = parser.add_mutually_exclusive_group()
		group.add_argument("-s","--save_recording", help="record capture", action = "store_true")
		group.add_argument("-p", "--play_recorded", help="use recroded capture", action= "store_true")

		args = parser.parse_args()

		if args.save_recording:
			return 'save'
		elif (args.play_recorded):
			return 'play'

	def camera_loop(self):
		while(True):
			loop_time = time.time()
			#pdb.set_trace()
			ret, frame = self.cap.read()
			#convert numpy matrix to represent HSV matrix
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#make a mask that has low red and upper red hue bounds
			mask = cv2.inRange(hsv, self.lower_red, self.upper_red)
			#apply mask to our image
			res = cv2.bitwise_and(hsv, hsv, mask = mask)
			#split up resultant 3 channel image
			[h , s, v] = cv2.split(res)
			#combine to get single channel gray scale
			thresh = cv2.bitwise_or(s, v)
			#binary threshold the image
			ret,thresh = cv2.threshold(thresh, 200, 255, 0)
			#find the edges of the binary image
			im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
			contours = np.array(contours)
			frame = cv2.drawContours(frame, contours, -1, color = (255,0,0), thickness = 3)
			
			#erode to try further isolate noise
			erosion_size = 5
			erosion_type = cv2.MORPH_ELLIPSE 
			element = cv2.getStructuringElement(erosion_type, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
			eroded = cv2.erode(frame, element)

			#blur image to low_pass filter
			blur = cv2.GaussianBlur(frame, (11,11), 0)
			#print(contours)
			# hull = cv2.convexHull(contours[0])

			# frame = cv2.drawContours(frame, hull, -1, color = (0,255,0), thickness = 3)

			#get convex 
			loop_time = time.time() - loop_time
			cv2.putText(blur, str(1/loop_time), self.bottom_left_corner, self.font, 1, self.font_color, self.line_type)

			cv2.imshow('frame', blur)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		self.cap.release()
		cv2.destroyAllWindows()		

#calling it as its own main for now, will be invoked by servo or some other parent later
cam = Camera()