import cv2
import numpy as np
import time
import argparse
import pdb
import visual_servo
#argument parsing

class Camera():
	def __init__(self):
		#run_state = self.parse_args()
		self.camera_init()
		self.mask_init()
		self.servo_controller = visual_servo.visual_servo()
		
		self.ball_pos_index_size = 5
		self.ball_pos_x = np.zeros(self.ball_pos_index_size)
		self.ball_pos_y = np.zeros(self.ball_pos_index_size)
		self.ball_pos_index = 0
		self.servo_controller.servo2.set_speed(20)
		self.servo_controller.servo1.set_speed(20)
		self.servo_controller.servo2.set_accel(0)
		self.servo_controller.servo1.set_accel(0)

		self.err_bound = 1
		self.accel = 5
		self.vel_x = 300
		self.vel_y = 100		

		self.camera_loop()

	#initializes a few camera parameters
	def camera_init(self):
		self.cap = cv2.VideoCapture('/dev/video2')
		camera_freq = self.cap.get(cv2.CAP_PROP_FPS)
		self.img_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		# print("width is " + str(self.img_width))
		self.img_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		# print("heigh is " + str(self.img_height))
		self.img_center = (self.img_width/2, self.img_height/2)		
		# print("center is at " + str(self.img_center))

		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.bottom_left_corner = (10, 440)
		self.font_color = (255,0,0)
		self.line_type = 2

	#initializes mask upper and lower thresholds, used in frame processing
	def mask_init(self):
		self.lower_red = np.array([15, 20, 230])
		self.upper_red = np.array([40, 155, 255])

	#argument processor, currently not utilized
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

	#this function will take the ball position and avergae it
	def ball_tracker(self, pos):
		#going to attempt to moving average over 5 frames
		x = pos[0]
		y = pos[1]
		if self.ball_pos_x[self.ball_pos_index] == 0:
			self.ball_pos_x[self.ball_pos_index] = x
			self.ball_pos_y[self.ball_pos_index] = y
			self.ball_pos_index = (self.ball_pos_index + 1) % self.ball_pos_index_size
			return (np.average(self.ball_pos_x[:self.ball_pos_index]), np.average(self.ball_pos_y[:self.ball_pos_index]) )
		else:
			self.ball_pos_x[self.ball_pos_index] = x
			self.ball_pos_y[self.ball_pos_index] = y
			self.ball_pos_index = (self.ball_pos_index + 1) % self.ball_pos_index_size
			return (np.average(self.ball_pos_x), np.average(self.ball_pos_y))

	#camera movement control function
	def move_camera_center(self, pos):
		frame_x_err = -1 * (self.img_center[0] - pos[0])
		frame_y_err = -1 * (self.img_center[1] - pos[1])

		servo1_pos = self.servo_controller.servo1.get_position()
		servo2_pos = self.servo_controller.servo2.get_position()

		if (frame_x_err > self.err_bound or frame_x_err < -(self.err_bound)):
			norm_error_x = frame_x_err/float(self.img_width/2)
			cub_of_norm = np.power(norm_error_x, 3)	
			self.servo_controller.servo1.go_to_position(servo1_pos + int(cub_of_norm * self.vel_x))

		if (frame_y_err > self.err_bound or frame_y_err < -(self.err_bound)):
			norm_error_y = frame_y_err/float(self.img_height/2)
			cub_of_norm = np.power(norm_error_y, 3)
			self.servo_controller.servo2.go_to_position(servo2_pos + int(cub_of_norm * self.vel_y))


	#captures and processes frame
	def frame_read(self):
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
		ret,thresh = cv2.threshold(thresh, 127, 255, 0)
		#find the edges of the binary image
		im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

		frame = cv2.GaussianBlur(frame, (5,5), 0)

		erosion_size = 5
		erosion_type = cv2.MORPH_ELLIPSE 
		element = cv2.getStructuringElement(erosion_type, (2*erosion_size + 1, 2*erosion_size+1), (erosion_size, erosion_size))
		frame = cv2.erode(frame, element)

		#frame = cv2.drawContours(frame, contours, -1, color = (255,0,0), thickness = 1)
		
		#get largest contour
		mid_x = None
		mid_y = None
		if len(contours) != 0:
			c = max(contours, key = cv2.contourArea)
			#check if this is actually circularizing like we think it is
			convex_hull = cv2.convexHull(c)
			cv2.drawContours(frame, convex_hull, -1, color = (255,0,0), thickness = 3)
			x,y,w,h = cv2.boundingRect(convex_hull)

			if isinstance(x, int) and isinstance(y,int):
				#print((x,y))
				cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	    		mid_x = int(x + w/2)
	    		mid_y = int(y + h/2)

	    		cv2.line(frame, (mid_x,0), (mid_x, self.img_height), (0,255,0), 2)
	    		cv2.line(frame, (0,mid_y), (self.img_width, mid_y), (0,255,0), 2)
	    		cv2.putText(frame, str((mid_x,mid_y)), self.bottom_left_corner, self.font, 1, self.font_color, self.line_type)
	    	else:
	    		self.state = 'searching'
		cv2.imshow('frame', frame)
		return (mid_x, mid_y)

	#main loop of application
	def camera_loop(self):
		while(True):
			ball_pos = self.frame_read()
			
			if ball_pos != (None, None):
				ave_pos = self.ball_tracker(ball_pos)
				self.move_camera_center(ave_pos)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		self.cap.release()
		cv2.destroyAllWindows()		

#calling it as its own main for now, will be invoked by servo or some other parent later
cam = Camera()
cam.servo_controller.close()