import serial

ser = serial.Serial('/dev/ttyACM0',115200)
ser.write("\xFE\x42")
ser.close()
