# import serial
import sys 
import textwrap

# ser = serial.Serial('/dev/ttyACM0',115200)
# ser.write("\xFE\x42")
# ser.close()

# import gfx.logo as logo

# print("data: ")
# print(logo.data)
# sys.stdout.flush()

print(textwrap.fill("Welcome to the Open City Project! Sharing sweet things to do", 18))
sys.stdout.flush()
