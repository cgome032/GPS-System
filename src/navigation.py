#
# Main file for Navigation system
#
#
#
#

# Libraries for drawing images
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Library for ST7737 controller
import ST7735 as TFT

# Library for GPIO for Raspberry Pi
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# Library for GPS
#import gpsd
from gps3 import gps3

# Library for time
import time

# Constants for system
#################################

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000


# Raspberry Pi configuration pins
DC = 24 # A0 on the TFT screen
RST = 25 # Reset pin on TFT screen
SPI_PORT = 0 # SPI port on raspberry pi, SPI0
SPI_DEVICE = 0 # Slave select on rapsberry pi, CE0

# Create TFT LCD display object
disp = TFT.ST7735(DC, rst=RST,spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE,max_speed_hz=SPEED_HZ))

# Initialize display
disp.begin()

# Background will be set to green
disp.clear((0,255,0))

rVal = 0
gVal = 0
bVal = 0

while True:
    disp.clear((rVal,gVal,bVal))
    disp.display()
    time.sleep(.5) # Wait time will be taken in seconds
    rVal += 10
    gVal += 10
    bVal += 10
    if(rVal > 255):
        rVal = 0
        gVal = 0
        bVal = 0

