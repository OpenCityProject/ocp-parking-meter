#!/usr/bin/python
import json
import sys
import subprocess
# import serial
# from Adafruit_Thermal import *
import urllib2

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

button = {'SELECT': 1, 'NEXT': 2, 'CANCEL': 3};

class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    printer = ""
    base_url = "http://opencityproject.australiasoutheast.cloudapp.azure.com:38080/v1"
    #debug = False
    debug = True

    def send_request(self, category, latitude, longitude):
        # just print instead of sending get request for now
        print "Sending request with parameters {{ category: {0}, latitude: {1}, longitude: {2} }}".format(category, latitude, longitude)
        # await response from server
        # poi_list = ["Cathedral Square", "Canterbury Museum", "Botanic Gardens"] # mock response for now
        response = json.loads(urllib2.urlopen(self.base_url + "/poi-by-category?lat=0&long=0&radiusInMetre=1000000000000&category=" + category).read())
        poi_list = response
        return poi_list

    def get_categories(self):
        response = json.loads(urllib2.urlopen(self.base_url + "/category").read())
        self.categories = response;

    def newLine(self, previousText):
        if self.debug == False: self.ser.write("\x0A")
    #    if self.debug == False: self.ser.write("_" * (20 - len(previousText))))

    def display(self, text):
        # for now just print to console
        print text
        # try send to serial
        if self.debug == False: self.ser.write(text)
        self.newLine(text)

    def newLCDPage(self, numberOfLinesRemaining):
        # self.ser.write("\xFE\x58")
        for i in range(numberOfLinesRemaining):
            if self.debug == False: self.ser.write("\x0A")
            print ""
        

    def get_choice(self):
        return input("") # change this to receive input from buttons on parking machine

    def print_ticket(self, poi):
        print "\n{0}'s sweet free thing is at {1}".format(poi.get("author"), poi.get("address"))
        print "It is: " + poi.get("name")
        print "It is sweet because: " + poi.get("description")
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
        self.printer.println("{0}'s sweet free thing is at {1}".format(poi.get("author"), poi.get("address")))
        self.printer.println("It is: " + poi.get("name"))
        self.printer.println("It is sweet because: " + poi.get("description"))
        self.printer.println("Open today: TODO")
        self.printer.feed(2)
        import gfx.adaqrcode as adaqrcode
        self.printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)
        self.printer.setSize('S')
        self.printer.println("For more info and to share your sweet free thing, see opencity.co.nz")
        self.printer.sleep()      # Tell printer to sleep
        self.printer.wake()       # Call wake() before printing again, even if reset
        self.printer.setDefault() # Restore printer to defaults

    def make_poi_selection(self, poi_list):
        if len(poi_list) == 0:
            print "============================================="
            self.display("Sorry, nothing found for that category")
            self.newLCDPage(3)
            print "============================================="
        else:
            starting_poi_pointer = 0
            ending_poi_pointer = 3
            choice = 2
            pois_length = len(poi_list)
            init = True
            while choice == 2:
                print "=============================================" # category screen
                if init == True:
                     self.display("Select an option:")
                for i in range(starting_poi_pointer, ending_poi_pointer):
                    select_marker = " <" if i == starting_poi_pointer else ""
                    self.display("{0}) {1}{2}".format(i%pois_length+1, poi_list[i%pois_length].get("name"), select_marker))
                print "============================================="
                sys.stdout.flush()
                choice = self.get_choice()
                starting_poi_pointer += 1
                ending_poi_pointer += 1
                if init == True:
                    ending_poi_pointer += 1 # add 1 more after initial screen page
                init = False

            if choice == 3: # Cancel
                return
            
            if choice == 1:
                self.print_ticket(poi_list[starting_poi_pointer-1])

    def start(self):
        print "Note: Set debug=False and uncomment import lines when testing on real rpi"
        print "=============================================="
        print "For cmd line testing, please type one of the keys below, then hit enter:"
        print "Key: '1' = Select Button"
        print "Key: '2' = Next Button"
        print "Key: '3' = Cancel Button"
        print "Press any of these to start (LCD backlight should be off until button pressed)"
        print "=============================================="
        sys.stdout.flush()        
        if self.debug == False: self.printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
        if self.debug == False: self.printer.setDefault()
        if self.debug == False: self.ser = serial.Serial('/dev/ttyACM0', 115200)
        if self.debug == False: self.ser.write("\xFE\x42")
        self.get_categories()
        self.get_choice()
        sys.stdout.flush()
        print "============================================="
        self.display("Welcome to Open City") # 20 characters
        self.display("Select a category:") # 19 characters
        self.display("(Press next)")
        self.newLCDPage(1)
        print "============================================="
        sys.stdout.flush()
        
        choice = 0
        while choice != button['SELECT'] and choice != button['NEXT']: # either select or next button will progress to the initial category screen
            choice = self.get_choice()

        starting_category_pointer = 0
        ending_category_pointer = 4
        choice = 2
        categories_length = len(self.categories)
        while choice == 2:
            print "=============================================" # category screen
            for i in range(starting_category_pointer, ending_category_pointer):
                select_marker = " <" if i == starting_category_pointer else ""
                self.display("{0}) {1}{2}".format(i%categories_length+1, self.categories[i%categories_length].get("name"), select_marker))
            print "============================================="
            sys.stdout.flush()
            choice = self.get_choice()
            starting_category_pointer += 1
            ending_category_pointer += 1

        if choice == 3: # Cancel
            return

        if choice == 1:
            print "You chose " + self.categories[starting_category_pointer-1].get("name")
            poi_list = self.send_request(self.categories[starting_category_pointer-1].get("id"), 0.00, 0.00)
            self.make_poi_selection(poi_list)
       
        if self.debug == False: self.ser.write("\xFE\x46")
        if self.debug == False: self.ser.close()

instance = ParkingMeter()
instance.start()