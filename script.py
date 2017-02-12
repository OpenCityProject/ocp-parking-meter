    #!/usr/bin/python
import sys
import subprocess
import serial
from Adafruit_Thermal import *

class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    printer = ""

    def send_request(self, category, latitude, longitude):
        # just print instead of sending get request for now
        print "Sending request with parameters {{ category: {0}, latitude: {1}, longitude: {2} }}".format(category, latitude, longitude)
        # await response from server
        poi_list = ["Cathedral Square", "Canterbury Museum", "Botanic Gardens"] # mock response for now
        return poi_list

    def display(self, text):
        # for now just print to console
        print text
        # try send to serial
        self.ser.write(text)
        self.ser.write("\x0A")

    def get_choice(self):
        return input("Your choice: ") # change this to receive input from buttons on parking machine

    def print_ticket(self, poi):
        print "Printing ticket for " + poi
        # create ticket file
        self.printer.justify('C')
        self.printer.setSize('L')
        self.printer.println("Open City")
        self.printer.setSize('S')
        self.printer.underlineOn()
        self.printer.println("Sharing sweet free things to do")
        self.printer.underlineOff()
        self.printer.justify('L')
        self.printer.println("Wesley's sweet free thing is 5 mins walk at Rolleston Ave")
        self.printer.println("It is: " + poi)
        self.printer.println("The Canterbury Museum is a museum located in the central city of Christchurch, New Zealand in the city's Cultural Precinct")
        self.printer.println("Open today: 9am-5pm")
        self.printer.feed(3)
        import gfx.adaqrcode as adaqrcode
        self.printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)
        self.printer.feed(1)
        self.printer.setSize('S')
        self.printer.println("For more info and to share your sweet free thing, see opencity.co.nz")
        self.printer.feed(1)
        self.printer.sleep()      # Tell printer to sleep
        self.printer.wake()       # Call wake() before printing again, even if reset
        self.printer.setDefault() # Restore printer to defaults

    def make_poi_selection(self, poi_list):
        for index, item in enumerate(poi_list, start = 1):
            self.display("{0}) {1}".format(index, item))
        sys.stdout.flush()
        self.display("Please choose an option: ")
        choice = self.get_choice()
        if choice > 0 and choice <= len(poi_list):
            self.print_ticket(poi_list[choice-1])
        else:
            self.display("Sorry, invalid choice")

    def start(self):
        self.printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
        self.printer.setDefault()
        self.ser = serial.Serial('/dev/ttyACM0', 115200)
        self.ser.write("\xFE\x42")
        self.display("Welcome to Open City! Please choose a category and hit enter:")
        for index, item in enumerate(self.categories, start = 1):
            self.display("{0}) {1}".format(index, item))
        sys.stdout.flush()
        choice = self.get_choice()
        if choice > 0 and choice <= len(self.categories):
            print "You chose " + self.categories[choice-1] # for debugging
            poi_list = self.send_request(self.categories[choice-1], 0.00, 0.00)
            self.make_poi_selection(poi_list)
        else:
            self.display("Sorry, you chose an invalid category")
        self.ser.write("\xFE\x46")
        self.ser.close()

instance = ParkingMeter()
instance.start()