#!/usr/bin/python
import json
import sys
import urllib2
import datetime

class DataCollector:
    base_url = "http://opencity.org.nz/api/v2/parking_box/"

    def start(self):
        print "Sending request to ocp server"
        date = datetime.datetime.now().strftime ("%Y_%m_%d")
        # await response from server
        #response = json.loads(urllib2.urlopen(self.base_url).read())
        response = {"meta": "test", "items": []}
        # validate response

        # save
        jsonString = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
        with open("data/test_" + date + ".json", "w") as text_file:
            text_file.write(jsonString)

instance = DataCollector()
instance.start()