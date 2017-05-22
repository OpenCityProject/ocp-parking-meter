#import serial
import sys

# This script is used to test different settings on the LCD display for the raspberry pi
# > python testscript.py
# 
# Need to double check if it works.. should work but unsure if \x characters display correctly
# q = quit
# on = turn LCD backlight on
# off = turn LCD backlight off
# b = brightness (0-255)
# c = contract (0-255)
# t = enter text to send
# clr = clear display (untested)
# n = newline (untested)

command = ""
# uncomment the line below when testing with the actual parking meter LCD display 
#ser = serial.Serial('/dev/ttyACM0', 115200)
actual = 'ser' in vars()

while command != "q":
    if actual ==False: print "========================================================\n Please uncomment line 19 when testing with actual LCD \n========================================================"
    print "q = quit"
    print "on = turn LCD backlight on"
    print "off = turn LCD backlight off"
    print "b = brightness (0-255)"
    print "c = contract (0-255)"
    print "t = enter text to send"
    print "clr = clear display (untested)"
    print "n = newline (untested)"
    print "\n"
    print "Command: (q, on, off, b, c, t, clr, n):"
    sys.stdout.flush()
    command = raw_input("")
    print("Your command was: " + command)
    if command == "on": 
        if actual == True: ser.write("\xFE\x42")
        print("\xFE\x42")
    elif command == "off": 
        if actual == True: ser.write("\xFE\x46")
        print("\xFE\x46")
    elif command == "b":
        print("please enter brightness (0-255)")
        sys.stdout.flush()
        value = input("") 
        if actual == True: ser.write("\xFE\x99" + chr(value))
        print("\xFE\x99" + chr(value))
    elif command == "c":
        print("please enter contrast (0-255, 180-220 is good)")
        sys.stdout.flush()
        value = input("") 
        if actual == True: ser.write("\xFE\x99" + chr(value))
        print("\xFE\x50" + chr(value))
    elif command == "t":
        print("please enter text to send")
        sys.stdout.flush()
        text = raw_input("")
        if actual == True: ser.write(text)
        if actual == True: ser.write("\x0A")
        #if actual == True: ser.write("_" * (20 - len(text)))
        print("sending to serial: " + text)
        print("\x0A")
    elif command == "n":
      #  if actual == True: ser.write("\x0A")
        if actual == True: ser.write(" " * 20)
        print("\x0A")
    elif command == "clr":
        if actual == True: ser.write("\xFE\x58")
        print("\xFE\x58")

    sys.stdout.flush()
        