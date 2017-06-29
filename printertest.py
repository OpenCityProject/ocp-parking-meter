#!/usr/bin/python

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyUSB0", 19200, timeout=5)
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults

## centre all text - initially small size
printer.justify('C')
printer.setSize('S')

## print logo bitmap
import gfx.logo as logo
printer.printBitmap(logo.width, logo.height, logo.data)
printer.feed(2)

## first_name, suburb - small bold
printer.boldOn()
printer.println("Steve from Sumner said: ")
printer.boldOff()
printer.feed(1)

## title - large
printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
printer.println("Climb or sit on the most lovely tree")
printer.feed(1)

## what_makes_it_awesome - normal
printer.setSize('S')
printer.println("It's easy to climb no matter how big or small you are. Plus it looks cool.")
printer.feed(2)

## small bold
printer.boldOn()
printer.println("Where is it?")
printer.boldOff()
printer.feed(1)

## address
printer.println("Christchurch Botanical Gardens, Rolleston Avenue, Christchurch City Centre,")
printer.feed(1)
## how to find
printer.println("Head to the Botanical Gardens and follow the signs to the archery lawn. The tree is about half way down on the left hand side. ")
printer.feed(2)

printer.println("Distance away: 705m")  # distance
printer.println("Time required: 5-10 mins")  # how_long_to_allow
printer.println("Wellbeing: Take Notice")  # which_5_way
printer.println("Best for: All Ages")  # for_kids

printer.feed(10)
printer.setDefault() # Restore printer to defaults
printer.sleep()      # Tell printer to sleep

# # Test inverse on & off
# printer.inverseOn()
# printer.println("Inverse ON")
# printer.inverseOff()

# # Test character double-height on & off
# printer.doubleHeightOn()
# printer.println("Double Height ON")
# printer.doubleHeightOff()

# # Set justification (right, center, left) -- accepts 'L', 'C', 'R'
# printer.justify('R')
# printer.println("Right justified")
# printer.justify('C')
# printer.println("Center justified")
# printer.justify('L')
# printer.println("Left justified")

# # Test more styles
# printer.boldOn()
# printer.println("Bold text")
# printer.boldOff()

# printer.underlineOn()
# printer.println("Underlined text")
# printer.underlineOff()

# printer.setSize('L')   # Set type size, accepts 'S', 'M', 'L'
# printer.println("Large")
# printer.setSize('M')
# printer.println("Medium")
# printer.setSize('S')
# printer.println("Small")

# printer.justify('C')
# printer.println("normal\nline\nspacing")
# printer.setLineHeight(50)
# printer.println("Taller\nline\nspacing")
# printer.setLineHeight() # Reset to default
# printer.justify('L')

# # Barcode examples
# printer.feed(1)
# # CODE39 is the most common alphanumeric barcode
# printer.printBarcode("ADAFRUT", printer.CODE39)
# printer.setBarcodeHeight(100)
# # Print UPC line on product barcodes
# printer.printBarcode("123456789123", printer.UPC_A)

# # Print the 75x75 pixel logo in adalogo.py
# import gfx.adalogo as adalogo
# printer.printBitmap(adalogo.width, adalogo.height, adalogo.data)

# # Print the 135x135 pixel QR code in adaqrcode.py
# import gfx.adaqrcode as adaqrcode
# printer.printBitmap(adaqrcode.width, adaqrcode.height, adaqrcode.data)
# printer.println("Adafruit!")
# printer.feed(2)

# printer.setDefault() # Restore printer to defaults
# printer.sleep()      # Tell printer to sleep
