ocp-parking-meter
===================
Contains code that will run on parking meter. It should integrate with the parking meter peripherals and send requests to web service.

## Setup
- GPIO 25 is start button (button 1)  
- GPIO 17 is idea button (button 2)  
- GPIO 23 is print button (button 3)  
- Adafruit LCD backpack is used via serial port ttyACM0 at baud rate 115200  
- Adafruit Thermal Printer is used via serial port ttyUSB0 at baud rate 19200

## Instructions and use case
- normal running (not in background) `python script.py`  
- run in background `nohup python /home/pi/ocp-parking-meter/script.py >/dev/null 2>&1 &`  
- load new data `python data-collector.py`  
- load new data then auto start script `./data-loader-cron.sh`

## Crons
- Please set the following cron jobs  
- set backlight off every minute `*/1 * * * * /home/pi/ocp-parking-meter/backlight-cron.sh`  
- set script to check every hour and reboot if not running `0 * * * * /home/pi/ocp-parking-meter/script-rebooter-cron.sh`
- set script to reload data from server every day at midnight `0 0 * * * sudo /home/pi/ocp-parking-meter/data-loader-cron.sh`

## add to /etc/rc.local to start up the script when pi is booted  
- `nohup python /home/pi/ocp-parking-meter/script.py >/dev/null 2>&1 &`  