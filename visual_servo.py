import serial
import sys 

class visual_servo():
	def __init__(self):
		print("initializing serial port")
		self.ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 5)
		print("serial port open!")

		servo1 = servo(0, self.ser)
		servo2 = servo(1, self.ser)

		servo1.set_position(float(sys.argv[1]))
		servo2.set_position(float(sys.argv[2]))

		servo1.go_to_position()
		servo2.go_to_position()

	def close(self):
		self.ser.close()

class servo():
	def __init__(self, number, ser):
		self.motor_number = chr(number)
		self.set_pos = chr(0x84)
		self.ser = ser
	
	def set_position(self, position):
		self.position = position

	def go_to_position(self):
		#turn pos from 0 - 100 to 1000-2000
		ms = int(1000 + (self.position/100.0 * 1000)) * 4
		bin_ms = bin(ms)

		low_bin = ms & 0b1111111
		high_bin = (ms & 0b11111110000000) >> 7

		low_bits = chr(low_bin)
		high_bits = chr(high_bin)
		
		self.ser.write(self.set_pos + self.motor_number + low_bits + high_bits)

vis_serv = visual_servo()

vis_serv.close()
