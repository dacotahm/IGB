from time import sleep
import picamera
import os

#Picture settings
INTERVAL = 10 # In seconds
RESOLUTION = (1920, 1080)
QUALITY = 30 # Plenty good for jpeg
PICDIR = '/home/pi/TimeLapsePics/' # Save directory

# Check to see if the directories exist for pics
if not os.path.exists(PICDIR)
	os.makedirs(PICDIR)

with picamera.PiCamera() as camera:
	camera.resolution = RESOLUTION
	for filename in camera.capture_continuous(PICDIR + 'img{timestamp:%m-%d-%y_%H-%M-%s}.jpg', 
	format = 'jpeg', quality = QUALITY):
		sleep(INTERVAL)
	