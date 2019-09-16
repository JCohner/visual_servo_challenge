import serial
import sys 

class visual_servo():
	def __init__(self):
		print("initializing serial port")
		self.ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 5)
		print("serial port open!")
		self.set_position(float(sys.argv[1]))
		self.close()

	def set_position(self, pos):
		#turn pos from 0 - 100 to 1000-2000
		ms = int(1000 + (pos/100.0 * 1000)) * 4
		bin_ms = bin(ms)

		low_bin = ms & 0b1111111
		high_bin = (ms & 0b11111110000000) >> 7

		low_bits = chr(low_bin)
		high_bits = chr(high_bin)

		set_pos_command = chr(0x84)
		pick_motor_command = chr(0x0)
		self.ser.write(set_pos_command + pick_motor_command + low_bits + high_bits)





	def close(self):
		self.ser.close()



vis_serv = visual_servo()

#

#ser.close()
#ser.open()