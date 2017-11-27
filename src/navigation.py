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
currentS = "Current Speed: " # Speed string
totalDis = "Total Distance: " # Distance string
currentLoc = "Current Location: " # Location string

# Distance x and y coordinates
distX = 10
distY = 20

pointsList = []

# Speed x and y coordinates
speedX = 10
speedY = 40

# Location x and y coordiantes
locX = 10
locY = 60

conversionVal = 2.24

# Speed update function, returns string
def speedFunc():
    SpeedText = data_stream.TPV['speed']
    if (SpeedText != "n/a"):
        SpeedText = float(SpeedText) * conversionVal
        SpeedText = str(SpeedText) + " mph"
    return (SpeedText)


# Latitude update function, returns string
def latFunc():
    Latitude = data_stream.TPV['lat']
    if(Latitude == "n/a"):
        return 0
    else:
        return float(Latitude)

# Longitude update function, returns string 
def lonFunc():
    Longitude = data_stream.TPV['lon']
    if (Longitude == "n/a"):
        return 0
    else:
        return float(Longitude)

totalDistance = 0
def distFunc():
    global totalDistance
    newLat = latFunc()
    newLon = lonFunc()
    if(newLat == 0 or newLon == 0):
        return (totalDistance)
    else:
        pointsList.append((newLat,newLon))
        last = len(pointsList)-1
        if(last == 0):
            return 0
        else:
            totalDistance += coorDistance(pointsList[last-1],pointsList[last])
            return totalDistance

def coorDistance(point1, point2):
    # Aproximate radius of the Earth in kilometers
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

    distance = (earthRadius * c) * 0.62137

    return distance
    



# Screen output function
def output():
    # Clearing screen and applying background
    disp.clear((255,255,255))
    draw.rectangle((0,10,127,150),outline=(255,0,0),fill=(255,0,0))
    

    # place distance variable on screen
    draw.text((distX,distY),str(distFunc()),font=ImageFont.load_default())


    # place speed variable on screen
    draw.text((speedX,speedY),speedFunc(),font=ImageFont.load_default())
    
    # Display updates to screen
    disp.display()


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
        #draw.text((speedX,speedY),str(SpeedText),font=ImageFont.load_default())
        print('Latitude = ',data_stream.TPV['lat'])
        print('Longitude = ',data_stream.TPV['lon'])
        output()
        #disp.display()
        time.sleep(1) # Wait time will be taken in seconds

