#!/usr/bin/python
import json
import sys
import urllib2
import threading
import random
import subprocess
import time
import textwrap

import serial
from Adafruit_Thermal import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  
# GPIO 23 set up as input. It is pulled up to stop false signals  
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

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

button = {'START': 1, 'IDEA': 2, 'PRINT': 3}

# PRINTER_GPIO = 27
# GPIO.setup(PRINTER_GPIO, GPIO.OUT)


class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    printer = ""
    base_url = "http://opencityproject.australiasoutheast.cloudapp.azure.com:38080/v1"
    debug = False
    #debug = True
    buttonDebug = False
#    buttonDebug = True
    buttonPressed = 0
    trigger = threading.Event()
    dataMap = {}

    def newLine(self, previousText):
        if self.debug == False: self.ser.write("\x0D")
     #   if self.debug == False: self.ser.write(" " * (20 - len(previousText)))

    def display(self, raw_text):
        text_array = textwrap.wrap(raw_text, 18)
        i = 0
        while i < len(text_array) and i < 4: # max 4 lines
            text = text_array[i]
            print text
            # try send to serial
            if self.debug == False: self.ser.write(text.encode())
            self.newLine(text)
            i += 1

    def newLCDPage(self):
        print("============== NEW PAGE =================")
        if self.debug == False: self.ser.write("\xFE\x58")
        
    def buttonOnePressed(self, num):
        self.buttonPressed = 1
        self.trigger.set()

    def buttonTwoPressed(self, num):
        self.buttonPressed = 2
        self.trigger.set()
        
    def buttonThreePressed(self, num):
        self.buttonPressed = 3
        self.trigger.set()

    def get_choice(self):
        if self.buttonDebug == False:
            self.trigger.clear()
            self.trigger.wait()
            return self.buttonPressed
        else:
            return input("") # change this to receive input from buttons on parking machine

    # def check_print_cut(self):
    #     result = subprocess.check_output(['lpstat', '-o'])
    #     while result.find("1st"):
    #         time.sleep(0.5)
    #     print("pulsing cut")
    #     sys.stdout.flush()        
    #     GPIO.output(PRINTER_GPIO, GPIO.LOW) # cut

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
        self.display("Welcome to the Open City Project! Sharing sweet things to do")
        print "============================================="
        sys.stdout.flush()
        choice = self.get_choice()
        if choice == button["IDEA"]:
            startPointer = random.randint(0, self.dataMap.get("meta").get("total_count")-1)
            self.idea_state(startPointer)
        else:
            self.welcome_state()

    def idea_state(self, pointer):
        print "ENTERING IDEA STATE"
        self.newLCDPage()
        # get ideas from json db
        poi_list = self.dataMap.get("items")
        # poi_list = [{"name": "Bebop - light sculpture by Bill Culbert"}, {"name": "Garden next to Peacock Fountain"}, {"name": "Kate Sheppard Memorial to Women's Suffrage"}] # mock response for now
        self.display(poi_list[pointer].get("title"))
        sys.stdout.flush()
        nextPointer = pointer + 1
        if nextPointer >= len(poi_list):
            nextPointer = 0
        choice = self.get_choice()
        if choice == button["IDEA"]:
            self.idea_state(nextPointer)
        elif choice == button["PRINT"]:
            self.print_ticket(poi_list[pointer])
            self.welcome_state()
        else:
            self.welcome_state()



    def print_ticket(self, poi):
        self.newLCDPage()
        self.display("Printing.....")
        if self.debug == False:
            # start checking print queue
            # t1 = threading.Thread(target=self.check_print_cut)
            # t1.start()
            self.printer.wake()       # Call wake() before printing again, even if reset
            self.printer.setDefault() # Restore printer to defaults

            ## centre all text - initially small size
            self.printer.justify('C')
            self.printer.setSize('S')

            ## print logo bitmap
            import gfx.logo as logo
            self.printer.printBitmap(logo.width, logo.height, logo.data)
            self.printer.feed(2)
           # self.printer.println("{0}'s sweet free thing is at {1}".format("Bob", "1 Queen Street"))

            ## first_name, suburb - small bold
            self.printer.boldOn()
            self.printer.println(textwrap.fill("{0} from {1} said: ".format(poi.get("first_name"), poi.get("suburb")),32))
            self.printer.boldOff()
            self.printer.feed(1)

            ## title - large
            self.printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
            self.printer.println(textwrap.fill(poi.get("title"), 16))
            self.printer.feed(1)

            ## what_makes_it_awesome - normal
            self.printer.setSize('S')
            self.printer.println(textwrap.fill(poi.get("what_makes_it_awesome"), 32))
            self.printer.feed(2)

            ## small bold
            self.printer.boldOn()
            self.printer.println("Where is it?")
            self.printer.boldOff()
            self.printer.feed(1)

            ## address
            self.printer.println(textwrap.fill(poi.get("address"),32))
            self.printer.feed(1)
            ## how to find
            self.printer.println(textwrap.fill(poi.get("how_to_find"), 32))
            self.printer.feed(2)

            self.printer.println("Distance away: " + poi.get("distance"))  # distance
            self.printer.println("Time required: " + poi.get("how_long_to_allow"))  # how_long_to_allow
            self.printer.println("Wellbeing: " + poi.get("which_5_way"))  # which_5_way
            self.printer.println("Best for: " + poi.get("for_kids"))  # for_kids

            self.printer.feed(10)
            self.printer.setDefault() # Restore printer to defaults
            self.printer.sleep()      # Tell printer to sleep
            # t1.join()

            
    def start(self):
        GPIO.add_event_detect(25, GPIO.RISING, callback=self.buttonOnePressed)
        GPIO.add_event_detect(17, GPIO.RISING, callback=self.buttonTwoPressed)
        GPIO.add_event_detect(23, GPIO.RISING, callback=self.buttonThreePressed)

        # read json file
        with open('data/data_2017_06_15.json', 'r') as file:
            data=file.read().replace('\n', '')
        self.dataMap = json.loads(data)
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
