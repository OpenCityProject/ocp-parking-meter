#import serial
import sys

command = ""
#ser = serial.Serial('/dev/ttyACM0', 115200)
actual = 'ser' in vars()

while command != "q":
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
        #if actual == True: ser.write("_" * (20 - len(text))))
        print("sending to serial: " + text)
    elif command == "n":
        if actual == True: ser.write("\x0A")
        print("\x0A")
    elif command == "clr":
        if actual == True: ser.write("\xFE\x58")
        print("\xFE\x58")

    sys.stdout.flush()
        