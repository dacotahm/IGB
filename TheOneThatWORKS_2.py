import os
import datetime
import time
from time import strftime, gmtime
import serial
from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta

# Change this to change the save directory.  If you want to save to a
# thumb drive use something like the following:
#
# BBpicDir = '/media/pi/C015-B1AE1/BBCounterPics'
# Thumb drives are always in /media/pi/*

BBPicDir = '/home/pi/BBCounterPics/'
BBDataDir = '/home/pi/BBCounterTime/'

if not os.path.exists(BBPicDir):
    os.makedirs(BBPicDir)
    
if not os.path.exists(BBDataDir):
    os.makedirs(BBDataDir)
     
camera = PiCamera()
camera.resolution = (1024, 1024)

# USB ports face down (rotation = 0)
# If power cord is facing up, rotation = -90
camera.rotation = -90

camera.capture(BBPicDir + "TESTPIC" + time.strftime("%y-%m-%d_%H-%M-%S") + ".jpg", quality = 30)
    

ser = serial.Serial ('/dev/ttyUSB0',9600)

i=0
while 1:
    ser.readline()
    print(ser.readline())
    if ser.readline != '':
        print("OUCH!", strftime("%Y-%m-%d %H:%M:%S"))
        camera.capture(BBPicDir + "img " + time.strftime("%y-%m-%d_%H-%M-%S") + ".jpg", quality = 30)
        with open(BBDataDir + "EventTime.txt", mode='a') as file:
            file.write(strftime("BB Detected at: " + "%Y-%m-%d %H:%M:%S") + "\n")
        sleep(1)
