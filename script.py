#!/usr/bin/python
import sys

def send_request(category, latitude, longitude):
    # just print instead of sending get request for now
    print "Sending request with parameters {category: " + category + ", latitude: " + \
        str(latitude) + ", longitude: " + str(longitude) + "}"
    # await response from server
    poi_list = ["Cathedral Square", "Cantebury Museum", "Botanic Gardens"] # mock response for now
    return poi_list

def display(text):
    # for now just print to console
    print text

def get_choice():
    return input("Your choice: ") # change this to receive input from buttons on parking machine

def print_ticket(poi):
    print "Printing ticket for " + poi

def make_poi_selection(poi_list):
    for i in range(0, len(categories)):
        display(str(i+1) + ") " + poi_list[i])
    sys.stdout.flush()
    display("Please choose an option: ")
    choice = get_choice()
    if choice > 0 and choice <= len(poi_list):
        print_ticket(poi_list[choice-1])
    else:
        display("Sorry, invalid choice")

categories = ["Parks", "Gardens", "Sports fields"]
display("Welcome to Open City! Please choose a category and hit enter:")
for i in range(0, len(categories)):
    display(str(i+1) + ") " + categories[i])
sys.stdout.flush()
choice = get_choice()
if choice > 0 and choice <= len(categories):
    print "You chose " + categories[choice-1] # for debugging
    poi_list = send_request(categories[choice-1], 0.00, 0.00)
    make_poi_selection(poi_list)
else:
    display("Sorry, you chose an invalid category")
