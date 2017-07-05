#! /bin/bash

# first kill script running
killall -9 python

# change dir
cd /home/pi/ocp-parking-meter

# now call python script to load data
python /home/pi/ocp-parking-meter/data-collector.py

# now reboot script
/home/pi/ocp-parking-meter/script-rebooter-cron.sh
