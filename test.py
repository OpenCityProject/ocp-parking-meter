# import serial
import sys 

# ser = serial.Serial('/dev/ttyACM0',115200)
# ser.write("\xFE\x42")
# ser.close()

import gfx.logo as logo

print("data: ")
print(logo.data)
sys.stdout.flush()

