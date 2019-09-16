import serial
import sys 

class visual_servo():
	def __init__(self):
		print("initializing serial port")
		self.ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 9600, timeout = 5)
		print("serial port open!")
		self.set_position(int(sys.argv[1]))
		self.close()

	def set_position(self, pos):
		#turn pos from 0 - 100 to 1000-2000
		ms = int(1000 + (pos/100.0 * 1000))
		print(ms)
		bin_ms = bin(ms)
		print(bin_ms)
		low_bin = bin_ms[-8:-1]
		high_bin = bin_ms[2:-8]
		pad = ''.zfill(7 - len(high_bin))
		high_bin = pad + high_bin


		print(hex(int(low_bin, 2)))
		print(hex(int(high_bin, 2)))

		low_bin = chr(int(low_bin, 2))
		print(hex(ord(low_bin)))

		high_bin = chr(int(high_bin, 2))
		print(hex(ord(high_bin)))

		set_pos_command = chr(0x84)
		pick_motor_command = chr(0x0)
		print(set_pos_command+pick_motor_command)
		print(hex(ord(set_pos_command)) + hex(ord(pick_motor_command)) + hex(ord(low_bin)) + hex(ord(high_bin)))
		#self.ser.write(set_pos_command + pick_motor_command + chr(0x70) + chr(0x2E))
		self.ser.write("\x84\x00\x70\x2E")





	def close(self):
		self.ser.close()



vis_serv = visual_servo()

#

#ser.close()
#ser.open()