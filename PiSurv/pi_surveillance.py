# import packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import warnings
import datetime
import dropbox
import imutils
import json
import time
import cv2

# arguement parser
#
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required = True, help="/home/pi/PiSurv/conf.json")
args = vars(ap.parse_args())

# filter warnings, load config, 
# initialize dropbox
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# check to see if dropbox should be used
if conf["use_dropbox"]:
	# connect to DB
	client = dropbox.Dropbox(conf["dropbox_access_token"])
	print("[SUCCESS] Dropbox account linked")
	
# initialize camera
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size = tuple(conf["resolution"]))

# camera warmup
# timestamp and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab raw NumPy image array...
	# ...and timestamp it
	frame = f.array
	timestamp = datetime.datetime.now()
	text = "Unoccupied"
	
	# resize frame, grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlure(gray, (21, 21), 0)
	
	# if the average frame is None, initialize it
	if avg is None:
		print("[INFO] starting background model...")
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue
	
	# accumulate weighted average between frames and compute difference
	# between current and running average to 
	# detect motion
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
	
	# Threshold the delta image, dilate thresholded image to fill
	# in holes, find contours on threshold image
	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
		cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations = 2)
	cnts = cv2.findContours(thres.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	
	# loop over contours
	for c in cnts:
		# if contours is small, ignore it
		if cv2.contourArea(c) < conf["min_area"]:
			continue
			
		# compute bounding box, draw on frame,
		# update text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
		
	# draw text and timestamp on frame
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, "Room Status: P{}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	0.35, (0, 0, 255), 1)
	
	# check to see if room is occupied
	if text == "Occupied":
		# check to see if enough time has passed between image uploads
		if(timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			# increment the motion counter
			motionCounter += 1
			
			# check to see if number of frames with motion is
			# high enough
			if motionCounter >= conf["min_motion_frames"]:
				# check to see if dropbox should be used
				if conf["use_dropbox"]:
					# write temporary image file
					t = TempImage()
					cv2.imwrite(t.path, frame)
					
					# upload image to DB and clean up temporary image
					print("[UPLOAD] {}".format(ts))
					path = "/[{base_path}/{timestamp}.jpg".format(
						base_path=conf["dropbox_base_path"], timestamp=ts)
					client.files_upload(open(t.path, "rb").read(), path)
					t.cleanup()
					
				# update last uploaded timestamp
				# reset motion counter
				lastUploaded = timestamp
				motionCounter = 0
				
	# otherwise room is not occupied
	else:
		motionCounter = 0
		
	# check to see if the frames should display to screen
	if conf["show_video"]:
		# display security feed
		cv2.imshow("Security Feed", frame)
		key = cv2.waitKey(1) & 0xFF
		
		# if the 'q' key is pressed, break loop and quit
		if key == ord("q"):
			break
	
	# clear stream and prep for next frame
	rawCapture.truncate(0)
