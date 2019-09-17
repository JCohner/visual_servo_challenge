import cv2
import numpy as np
import time
import argparse

#argument parsing

class Camera():
	def __init__(self):
		self.parse_args()

		cap = cv2.VideoCapture('/dev/video2')
		camera_freq = cap.get(cv2.CAP_PROP_FPS)
		# self.img_width = cap.get(cv2.CAP_PROP_WIDTH)
		# self.img_height = cap.get(cv2.CAP_PROP_HEIGHT)		
		self.cap = cap

		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.bottom_left_corner = (10, 440)
		self.font_color = (255,255,255)
		self.line_type = 2

		self.camera_loop()

	def parse_args(self):
		parser = argparse.ArgumentParser()
		group = parser.add_mutually_exclusive_group()
		group.add_argument("-s","--save_recording", help="record capture", action = "store_true")
		group.add_argument("-p", "--play_recorded", help="use recroded capture", action= "store_true")


	def camera_loop(self):
		while(True):
			loop_time = time.time()
			
			ret, frame = self.cap.read()

			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			lower_red = np.array([0, 127, 127])
			upper_red = np.array([10, 255, 255])

			mask = cv2.inRange(hsv, lower_red, upper_red)

			res = cv2.bitwise_and(frame, frame, mask = mask)

			loop_time = time.time() - loop_time
			cv2.putText(hsv, str(1/loop_time), self.bottom_left_corner, self.font, 1, self.font_color, self.line_type)


			cv2.imshow('frame', res)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()		

#calling it as its own main for now, will be invoked by servo or some other parent later
cam = Camera()