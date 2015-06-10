
'''-----------------------------------------------------------------------------------------------------
Provides a generator to capture frames from a camera and store it in a location (destination).
Author: Sreeram 
Date: 04th May 2015
Modified: 04th May 2015
Logs: N/A

Usage:

import cv2
import numpy 
from cameraImage import *


destination="/home/sreeram/Pictures/camera.png" # destination to store 


ob1=cameraImage(camera=1,destination,skip_frames=0)  


for var in ob1:
	print var
	
	if var is not(None):

		cv2.imshow('camera frames',var)
		
		k=cv2.waitKey(1)
		if k==27:
			break


-----------------------------------------------------------------------------------------------------'''
import cv2
import numpy
'''-----------------------------------------------------------------------------------------------------
Type: Generator class
Inputs:


1. camera (Int) - The camera 
2. destination (string)- The file to which frame is to be stored
3. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
-----------------------------------------------------------------------------------------------------'''


class cameraImage(object):

	def __init__(self, camera, destination, skip_frames=0):

		'''

		Function 1 : __init__ (Initialisation)

		This function performs the following task:
		
		1. Initializes the cameraImage object and validates the input parameters.

		'''


		if type(camera) is not int:
			raise TypeError("Input Error:  Camera number should be an Integer.")

		self.cap = cv2.VideoCapture(camera)
		ret,frame = self.cap.read()

		if ret==False:
			raise TypeError("Not able to read frames from camera. Check camerRedis.py")

		if type(skip_frames) is not int:
			raise TypeError("skip_frames should be an integer")

		self.cap = cv2.VideoCapture(camera)
		self.destination=destination
		self.skip_frames = skip_frames
    
	def __iter__(self):
		return self

	def next(self):

		'''
		Function 2 : next

		This function grabs frames from camera and writes to the image destination 

		'''

		if self.cap.isOpened()==False: 
			raise StopIteration("Error. Check camera number. Camera object not available")


		for j in xrange(self.skip_frames):
			
			ret,frame = self.cap.read()
			
			if ret==False:
				raise StopIteration("Frames are not read by camera")
 


		ret,frame = self.cap.read()
		
		if ret==False:
			raise StopIteration("Frames are not read by camera")

		cv2.imwrite(self.destination,frame)
		
		return frame



if __name__ == "__main__":

	destination="/home/sreeram/Pictures/camera.png" # destination to store 


	ob1=cameraImage(2,destination,10)  


	for var in ob1:
		print var
		
		if var is not(None):

			cv2.imshow('camera frames',var)
			
			k=cv2.waitKey(1)
			if k==27:
				break

	




	
