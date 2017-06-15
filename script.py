#!/usr/bin/python
import json
import sys
import urllib2
import threading
import serial
from Adafruit_Thermal import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  
# GPIO 23 set up as input. It is pulled up to stop false signals  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

# This script is used to call the api then return choices to the user and display on LCD
# User first selects from a list of pre-defined categories
# Script will then make an api call to retrieve all nearby POIs of that category
# User can then select one of the POIs and machine will print a ticket
#
# > python script.py
# 
# Requires the base_url to be working and hosting the open city api - this is currently down so script will fail..
#
# Note: Uncomment the "import" lines and set debug=False when running on the actual rpi
# Note: Currently having problems with line wrapping and new line printing on the LCD display
# Note: Also, the buttons have not been integrated yet, so this script relies on keyboard input solely for now

button = {'START': 1, 'IDEA': 2, 'PRINT': 3};

class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    printer = ""
    base_url = "http://opencityproject.australiasoutheast.cloudapp.azure.com:38080/v1"
    debug = False
    #debug = True
#    buttonDebug = False
    buttonDebug = True
    buttonPressed = 0
    trigger = threading.Event()

    def send_request(self, category, latitude, longitude):
        # just print instead of sending get request for now
        print "Sending request with parameters {{ category: {0}, latitude: {1}, longitude: {2} }}".format(category, latitude, longitude)
        # await response from server
        poi_list = [{"name": "Bebop - light sculpture by Bill Culbert"}, {"name": "Garden next to Peacock Fountain"}, {"name": "Kate Sheppard Memorial to Women's Suffrage"}] # mock response for now
        #response = json.loads(urllib2.urlopen(self.base_url + "/poi-by-category?lat=0&long=0&radiusInMetre=1000000000000&category=" + category).read())
        #poi_list = response
        return poi_list

    def get_categories(self):
        #response = json.loads(urllib2.urlopen(self.base_url + "/category").read())
        response = [{"name": "Connect with Others"}, {"name": "Savour the Moment"}, {"name": "Play/Be Active"}, {"name": "Keep Learning"}, {"name": "Make a Difference"}]
        self.categories = response;

    def newLine(self, previousText):
        if self.debug == False: self.ser.write("\x0D")
     #   if self.debug == False: self.ser.write(" " * (20 - len(previousText)))

    def display(self, text, newLine):
        # for now just print to console
        print text
        # try send to serial
        if self.debug == False: self.ser.write(text)
        if newLine == True: self.newLine(text)

    def newLCDPage(self):
        print("============== NEW PAGE =================")
        if self.debug == False: self.ser.write("\xFE\x58")
        # self.ser.write("\xFE\x58")
        # for i in range(numberOfLinesRemaining):
        #     if self.debug == False: self.ser.write("\x0A")
        #     print ""
        
    def buttonOnePressed(self):
        self.buttonPressed = 1
        self.trigger.set()

    def buttonTwoPressed(self):
        self.buttonPressed = 2
        self.trigger.set()
        
    def buttonThreePressed(self):
        self.buttonPressed = 3
        self.trigger.set()

    def get_choice(self):
        if self.buttonDebug == False:
            self.trigger.clear()
            GPIO.add_event_detect(17, GPIO.RISING, callback=self.buttonOnePressed)  
            GPIO.add_event_detect(23, GPIO.RISING, callback=self.buttonTwoPressed)  
            GPIO.add_event_detect(24, GPIO.RISING, callback=self.buttonThreePressed) 
            self.trigger.wait()
            return self.buttonPressed
        else:
            return input("") # change this to receive input from buttons on parking machine

    def print_ticket(self, poi):
        self.newLCDPage()
        self.display("Printing.....", True)
        print "\n{0}'s sweet free thing is at {1}".format("Bob", "1 Queen Street")
        print "It is: " + poi.get("name")
        print "It is sweet because: It is pretty cool"
        sys.stdout.flush()
        if self.debug == False:
            self.printer.wake()       # Call wake() before printing again, even if reset
            self.printer.setDefault() # Restore printer to defaults
            # create ticket file
            self.printer.justify('C')
            self.printer.setSize('M')
            self.printer.println("Open City")
            self.printer.feed(1)
            self.printer.setSize('S')
            self.printer.underlineOn()
            self.printer.println("Sharing sweet free things to do")
            self.printer.underlineOff()
            self.printer.justify('L')
            self.printer.println("{0}'s sweet free thing is at {1}".format("Bob", "1 Queen Street"))
            self.printer.println("It is: " + poi.get("name"))
            self.printer.println("It is sweet because: It is pretty cool")
            self.printer.println("Open today: TODO")
            self.printer.feed(2)
            import gfx.adaqrcode as adaqrcode
            self.printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)
            self.printer.setSize('S')
            self.printer.println("For more info and to share your sweet free thing, see opencity.co.nz")
            self.printer.sleep()# Tell printer to sleep

    def sleep_state(self):
        print "ENTERING SLEEP STATE"
        sys.stdout.flush()
        choice = self.get_choice()
        # initially wake up screen if any button is pressed
        self.welcome_state()            

    def welcome_state(self):
        print "ENTERING WELCOME STATE"
        if self.debug == False: self.ser.write("\xFE\x42")
        self.newLCDPage()
        print "============================================="
        self.display("Welcome to the", True)
        self.display("Open City Project!", True)
        self.display("Sharing sweet", True)
        self.display("things to do", False)
        print "============================================="
        sys.stdout.flush()
        choice = self.get_choice()
        if choice == button["IDEA"]:
            self.idea_state(0)
        else:
            self.welcome_state()

    def idea_state(self, pointer):
        print "ENTERING IDEA STATE"
        self.newLCDPage()
        poi_list = [{"name": "Bebop - light sculpture by Bill Culbert"}, {"name": "Garden next to Peacock Fountain"}, {"name": "Kate Sheppard Memorial to Women's Suffrage"}] # mock response for now
        self.display(poi_list[pointer].get("name"), False)
        sys.stdout.flush()
        nextPointer = pointer + 1
        if nextPointer >= len(poi_list):
            nextPointer = 0
        choice = self.get_choice()
        if choice == button["IDEA"]:
            self.idea_state(nextPointer)
        elif choice == button["PRINT"]:
            self.print_ticket(poi_list[pointer])
            self.sleep_state()
        else:
            self.welcome_state()
            
    def start(self):
        try:
            print "Note: Set debug=False and uncomment import lines when testing on real rpi"
            print "=============================================="
            print "For cmd line testing, please type one of the keys below, then hit enter:"
            print "Key: '1' = START button"
            print "Key: '2' = IDEA Button"
            print "Key: '3' = PRINT Button"
            print "Press any of these to start (LCD backlight should be off until button pressed)"
            print "=============================================="
            sys.stdout.flush()        
            if self.debug == False: self.printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
            if self.debug == False: self.printer.setDefault()
            if self.debug == False: self.ser = serial.Serial('/dev/ttyACM0', 115200)

            self.sleep_state()
       
        except KeyboardInterrupt, Exception:
            print ("ctrl c pressed")
            self.newLCDPage()
            if self.debug == False: self.ser.write("\xFE\x46")
            if self.debug == False: self.ser.close()
            if self.debug == False: GPIO.cleanup()# clean up GPIO
        
        print ("Program exiting normally")        
        self.newLCDPage()
        if self.debug == False: self.ser.write("\xFE\x46")
        if self.debug == False: self.ser.close()
        if self.debug == False: GPIO.cleanup()# clean up GPIO
        

instance = ParkingMeter()
instance.start()
