#! /bin/bash

# first kill script running
killall -9 script.py

# now call python script to load data
python data-collector.py

# now reboot script
./script-rebooter-cron.sh