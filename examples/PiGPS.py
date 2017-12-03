#! /usr/bin/python3

import gpsd
import urllib.request 
import time

class Pigps:

    def __init__(self):
        # Connect to the local gpsd on the Pi
        gpsd.connect()

    def getCurrentPosition:
        self.packet = gpsd.get_current()
        print(self.packet.position())
        

    def getCurrentSpeed(self):
        self.packet = gpsd.get_current()
        print(self.)

    def getUrl(self):
        self.packet = gpsd.get_current()
        print(self.packet.map_url())



if __name__=='__main__':
    Pigps()
    Pigps.getCurrentPosition()
    Pigps.getCurrentSpeed()

    # Connect to the local gpsd
    gpsd.connect()

connectionString = packet.map_url()
print(connectionString)
# Open url page
# u = urllib.request.urlopen(connectionString)
