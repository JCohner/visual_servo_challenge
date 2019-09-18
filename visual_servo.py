import serial
import sys 


class visual_servo():
	def __init__(self):
		print("initializing serial port")
		self.ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 5)
		print("serial port open!")

		self.servo1 = servo(0, self.ser)
		self.servo2 = servo(1, self.ser)

	def close(self):
		self.ser.close()

class servo():
	def __init__(self, number, ser):
		self.motor_number = chr(number)
		self.ser = ser

	def go_to_position(self, position):
		#turn pos from 0 - 100 to 1000-2000
		#ms = int(1000 + (position/100.0 * 1000)) * 4
		#we are actually going to use the position specified by us/4
		ms = position

		#print(ms)

		set_pos = chr(0x84)

		low_bin = ms & 0b1111111
		high_bin = (ms & 0b11111110000000) >> 7

		low_bits = chr(low_bin)
		high_bits = chr(high_bin)
		
		self.ser.write(set_pos + self.motor_number + low_bits + high_bits)

	def get_position(self):

		get_pos = chr(0x90)
		self.ser.write(get_pos + self.motor_number)

		byte1 = self.ser.read(1)
		byte2 = self.ser.read(1)

		# print((byte1,byte2))
		byte1 = ord(byte1)
		byte2 = ord(byte2)



		pos = (byte2 << 8) | byte1

		return pos

	def set_speed(self, speed):
		set_speed = chr(0x87)
		speed = int(speed) #in 0.25us/10ms

		low_bin = speed & 0b1111111
		high_bin = (speed & 0b11111110000000) >> 7

		low_bits = chr(low_bin)
		high_bits = chr(high_bin)

		self.ser.write(set_speed + self.motor_number + low_bits + high_bits)

