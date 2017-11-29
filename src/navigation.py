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

# Library for finding distance between two points
from math import sin, cos, sqrt, atan2, radians

# Import Rpi library to use buttons to switch menus and reset
#
import RPi.GPIO as bGPIO

# Setup pins for buttons

bGPIO.setmode(bGPIO.BCM)
bGPIO.setup(18,bGPIO.IN,pull_up_down=bGPIO.PUD_DOWN)

bGPIO.setup(23,bGPIO.IN,pull_up_down=bGPIO.PUD_DOWN)

# import geopy library for Geocoding
#
# Internet access is necessary for this to work

from geopy.geocoders import Nominatim

geolocator = Nominatim()

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
#disp.clear((0,255,0))


# Clear screen to white and display
#disp.clear((255,255,255))
draw = disp.draw()
#draw.rectangle((0,10,127,150),outline=(255,0,0),fill=(0,0,255))
#disp.display()

# Speed, Latitude, Longitude placement variables
#currentS = "Current Speed: " # Speed string
#totalDis = "Total Distance: " # Distance string
#currentLoc = "Current Location: " # Location string

# Distance x and y coordinates
distX = 10
distY = 20

pointsList = []

# Speed x and y coordinates
speedX = 10
speedY = 20

# Location x and y coordiantes
locX = 10
locY = 60

# Converts from m/s to mph
conversionVal = 2.24

# Speed update function, returns string

speedVar = 0
def speedFunc():
    global speedVar
    SpeedText = data_stream.TPV['speed']
    if (SpeedText != "n/a"):
        SpeedText = float(SpeedText) * conversionVal
        SpeedVar = round(SpeedText,0)
    # return (SpeedText)



def locationFunc():
    latLoc = latFunc()
    lonLoc = lonFunc()

# Latitude update function, returns float value
def latFunc():
    Latitude = data_stream.TPV['lat']
    if(Latitude == "n/a"):
        return 0
    else:
        return float(round(Latitude,4))

# Longitude update function, returns string 
def lonFunc():
    Longitude = data_stream.TPV['lon']
    if (Longitude == "n/a"):
        return 0
    else:
        return float(round(Longitude,4))

# Distance function returns TOTAL distance travelled

totalDistance = 0

def distFunc():
    global totalDistance
    newLat = latFunc()
    newLon = lonFunc()
    if(newLat == 0 or newLon == 0):
        totalDistance = totalDistance
        # return (totalDistance)
    else:
        pointsList.append((newLat,newLon))
        last = len(pointsList)-1
        if(last == 0):
            return 
        else:
            totalDistance += coorDistance(pointsList[last-1],pointsList[last])
            # return totalDistance

# Resets total distance 

def resDistance():
    global totalDistance
    totalDistance = 0


# Function used to find distance between two coordinates
# uses Haversine's formula to find.
# Input points are a tuple

def coorDistance(point1, point2):
    # Approximate radius of the Earth in kilometers
    earthRadius = 6373.0

    lat1 = point1[0]
    lon1 = point1[1]

    lat2 = point2[0]
    lon2 = point2[1]

    distanceLon = lon2 - lon1
    distanceLat = lat2 - lat1

    # Haversine a
    a = sin(distanceLat/2)**2 + cos(lat1) * cos(lat2) * sin(distanceLon/2)**2

    # Haversine c
    c = 2 * atan2(sqrt(a),sqrt(1-a))

    # Convert km to Miles
    distance = (earthRadius * c) * 0.62137

    if(distance <= 0.01):
        return 0.00
    else:
        return round(distance,3)


# Function to display speed on screen

def dispSpeed():
    
    # Place distance on variable on screen
    draw.text((speedX,speedY),str(speedVar),font=ImageFont.truetype("Lato-Medium.ttf",72))

# Function to display distance on screen

def dispDistance():
    draw.text((distX,distY),str(totalDistance),font=ImageFont.truetype("Lato-Medium.ttf",60))

# Function ti display location on screen, requires internet to work

def dispLocation():

    return 0

# Using dictionary to mimic switch statements

dispOptions = {
        0 : dispSpeed,
        1 : dispDistance,
        3 : dispLocation
}


# Screen output function

def output():
    # Using global variable for displayIndex
    global displayIndex
    # Clearing screen and applying background
    disp.clear((255,255,255))
    draw.rectangle((0,10,127,150),outline=(255,0,0),fill=(255,0,0))

    # Calls function depending on displayIndex value
    dispOptions[displayIndex]()

    
    # Will erase if other method works

    # place distance variable on screen
    #draw.text((distX,distY),str(distFunc()),font=ImageFont.load_default())
    # place speed variable on screen
    #draw.text((speedX,speedY),speedFunc(),font=ImageFont.load_default())
    
    # Display updates to screen
    disp.display()


displayButton = 18 # BCM Pin on raspberry pi
resetButton = 23 # BCM Pin on raspberry pi

buttonPress = False

def checkDisplay():
    global buttonPress
    global displayIndex
    if(bGPIO.input(displayButton) and not buttonPress):
        displayIndex += 1
        buttonPress = True
        if(displayIndex == 2):
            displayIndex = 0
    elif(bGPIO.input(displayButton) and buttonPress):
        print ("Still pressed")
    else:
        buttonPress = False
    

# Setup gps
gps_socket=gps3.GPSDSocket()
data_stream=gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

timerPeriod = .1
# Index value for display
displayIndex = 0
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print('Latitude = ',data_stream.TPV['lat'])
        print('Longitude = ',data_stream.TPV['lon'])
        distFunc()
        speedFunc()
        output()
        checkDisplay()
        if(bGPIO.input(resetButton)):
            resDistance()
        time.sleep(timerPeriod) # Wait time will be taken in seconds

