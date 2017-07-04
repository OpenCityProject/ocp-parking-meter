#!/usr/bin/python
import json
import sys
import urllib2
#import datetime

class DataCollector:
    base_url = "https://beta.opencity.org.nz/api/v2/parking_box/"

    def start(self):
        print "Sending request to ocp server"
        #date = datetime.datetime.now().strftime ("%Y_%m_%d")
        # await response from server
        response = json.loads(urllib2.urlopen(self.base_url).read())
        # validate response
        if len(response.get("items")) > 0:
            # save
            print("Saving {0} items to json file".format(len(response.get("items"))))
            jsonString = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
            with open("data/data.json", "w") as text_file:
                text_file.write(jsonString)
        else:
            print("Error: no items in response")
            #print("Error: total_count does not match number of items, not saving");
            
instance = DataCollector()
instance.start()