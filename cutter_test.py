import subprocess
import time
from Adafruit_Thermal import *
import RPi.GPIO as GPIO
import threading
import sys

GPIO.setmode(GPIO.BCM)  
PRINTER_GPIO = 27
GPIO.setup(PRINTER_GPIO, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)

def check_print_cut():
    result = ""
    while result.find("1st"):
        result = subprocess.check_output(['lpstat', '-o'])
        print(result)
        sys.stdout.flush()        
        time.sleep(0.5)
    print("pulsing")
    sys.stdout.flush()        
    GPIO.output(PRINTER_GPIO, GPIO.LOW)

t1 = threading.Thread(target=check_print_cut)
t1.start()
printer.wake()
printer.println("Open City")
printer.println("Test")
printer.println("1")
printer.println("2")
printer.println("3")
printer.feed(2)
printer.sleep()
t1.join()

print("done")
sys.stdout.flush()        
