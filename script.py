    #!/usr/bin/python
import json
import sys
import subprocess
# import serial
# from Adafruit_Thermal import *
import urllib2

class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    printer = ""
    base_url = "http://opencityproject.australiasoutheast.cloudapp.azure.com/v1"
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

    def display(self, text):
        # for now just print to console
        print text
        # try send to serial
        if self.debug == False: self.ser.write(text)
        if self.debug == False: self.ser.write("\x0A")

    def get_choice(self):
        return input("Your choice: ") # change this to receive input from buttons on parking machine

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
            self.display("Sorry, nothing found for that category")
        else:
            for index, item in enumerate(poi_list, start = 1):
                self.display("{0}) {1}".format(index, item.get("name")))
            sys.stdout.flush()
            self.display("Please choose an option: ")
            choice = self.get_choice()
            if choice > 0 and choice <= len(poi_list):
                self.print_ticket(poi_list[choice-1])
            else:
                self.display("Sorry, invalid choice")

    def start(self):
        if self.debug == False: self.printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
        if self.debug == False: self.printer.setDefault()
        if self.debug == False: self.ser = serial.Serial('/dev/ttyACM0', 115200)
        if self.debug == False: self.ser.write("\xFE\x42")
        self.get_categories()
        self.display("Welcome to Open City! Please choose a category and hit enter:")
        for index, item in enumerate(self.categories, start = 1):
            self.display("{0}) {1}".format(index, item.get("name")))
        sys.stdout.flush()
        choice = self.get_choice()
        if choice > 0 and choice <= len(self.categories):
            print "You chose " + self.categories[choice-1].get("name") # for debugging
            poi_list = self.send_request(self.categories[choice-1].get("id"), 0.00, 0.00)
            self.make_poi_selection(poi_list)
        else:
            self.display("Sorry, you chose an invalid category")
        if self.debug == False: self.ser.write("\xFE\x46")
        if self.debug == False: self.ser.close()

instance = ParkingMeter()
instance.start()