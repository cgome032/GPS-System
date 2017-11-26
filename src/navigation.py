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


# Clear screen to while and display
disp.clear((255,255,255))
draw = disp.draw()
draw.rectangle((0,10,127,150),outline=(255,0,0),fill=(0,0,255))
disp.display()

# Speed, Latitude, Longitude placement variables
currentS = "CURRENT SPEED: "
speedX = 10
speedY = 20

# Speed update function, returns string
def speedFunc():
    SpeedText = data_stream.TPV['speed']
    return str(SpeedText)


# Latitude update function, returns string
def latFunc():
    Latitude = data_stream.TPV['lat']
    return str(Latitude)

# Longitude update function, returns string 
def lonFunc():
    Longitude = data_stream.TPV['lon']
    return str(Longitude)

# Screen output function
def output():
    disp.clear((255,255,255))
    draw.rectangle((0,10,127,150),outline=(255,0,0),fill=(255,0,0))


# Setup gps
gps_socket=gps3.GPSDSocket()
data_stream=gps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        #SpeedText = data_stream.TPV['speed']
        #Latitude = data_stream.TPV['lat']
        #Longitude = data_stream.TPV['lon']
        draw.text((speedX,speedY),str(SpeedText),font=ImageFont.load_default())
        print('Latitude = ',data_stream.TPV['lat'])
        print('Longitude = ',data_stream.TPV['lon'])
        disp.display()
        time.sleep(1) # Wait time will be taken in seconds

