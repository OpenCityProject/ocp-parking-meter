    #!/usr/bin/python
import json
import sys
import subprocess
#import serial
import urllib2

class ParkingMeter:
    categories = ["Get Back to Nature", "Within 2km", "Give Back to Community", "Today only", "Weekly"]
    ser = ""
    debug = True
    #debug = False


    def send_request(self, category, latitude, longitude):
        # just print instead of sending get request for now
        print "Sending request with parameters {{ category: {0}, latitude: {1}, longitude: {2} }}".format(category, latitude, longitude)
        response = json.loads(urllib2.urlopen("http://opencityproject.australiasoutheast.cloudapp.azure.com/v1/poi?lat=0&long=0").read())
        poi_list = list(poi.get("name") for poi in response)
        return poi_list

    def display(self, text):
        # for now just print to console
        print text
        # try send to serial
        if self.debug == False: self.ser.write(text)
        if self.debug == False: self.ser.write("\x0A")

    def get_choice(self):
        return input("Your choice: ") # change this to receive input from buttons on parking machine

    def print_ticket(self, poi):
        print "Printing ticket for " + poi

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
        if self.debug == False: elf.ser = serial.Serial('/dev/ttyACM0', 115200)
        if self.debug == False: self.ser.write("\xFE\x42")
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
        if self.debug == False: self.ser.write("\xFE\x46")
        if self.debug == False: self.ser.close()

instance = ParkingMeter()
instance.start()