import cv2
import numpy as np
import time

cap = cv2.VideoCapture('/dev/video2')
camera_freq = cap.get(cv2.CAP_PROP_FPS)
print(camera_freq)

font = cv2.FONT_HERSHEY_SIMPLEX
bottom_left_corner = (10, 440)
font_color = (255,255,255)
line_type = 2

while(True):
	loop_time = time.time()
	
	ret, frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_red = np.array([0, 127, 127])
	upper_red = np.array([10, 255, 255])

	mask = cv2.inRange(hsv, lower_red, upper_red)

	res = cv2.bitwise_and(frame, frame, mask = mask)

	loop_time = time.time() - loop_time
	cv2.putText(hsv, str(1/loop_time), bottom_left_corner,font, 1, font_color, line_type)


	cv2.imshow('frame', res)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
