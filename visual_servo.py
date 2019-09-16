import serial

ser = serial.Serial(port = '/dev/ttyACM1', baudrate = 9600)
print("serial port open!")
ser.close()
#ser.open()