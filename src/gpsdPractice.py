#! /usr/bin/python3

import gpsd
import urllib.request 
import time

# Connect to the local gpsd
gpsd.connect()

# Get gps position
packet = gpsd.get_current()

while True:
    print(packet.speed())
    time.sleep(10)
