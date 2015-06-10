
'''-----------------------------------------------------------------------------------------------------
Provides a generator to  capture frames from a camera, and load it to a numpy array.
Author: Sreeram Menon
Date: 04th May 2015
Modified: 04th May 2015
Logs: N/A

Usage: 


import numpy
import cv2
from cameraArray import *

ob1=cameraArray(camera=1, skip_frames=0, bundle_frames=1)  # creating object

for var in ob1:
	print var
	cv2.imshow("camera",var)
	k=cv2.waitKey(1)
	if k==27:
		break


-----------------------------------------------------------------------------------------------------'''

import numpy
import cv2

'''-----------------------------------------------------------------------------------------------------
Name: cameraArray
Type: Generator class
Inputs:


1. camera (Int) [defaults - 0] - The camera Number
2. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
3. bundle_frames (int) [defaults - 1] - Number of frames to bundle when value is returned
-----------------------------------------------------------------------------------------------------'''


class cameraArray(object):

	def __init__(self, camera=1, skip_frames=0, bundle_frames=1):

		'''

		Function 1 : Initilisation

		This function perfoms the following tasks:

		1. Initialise camera capture object
		2. Set values for skip_frames and bundle_frames


		'''

		if type(camera) is not int:
			raise TypeError("Input Error:  Camera number should be an Integer.")

		self.cap = cv2.VideoCapture(camera)

		if type(skip_frames) is not int:
			raise TypeError("Input Error:  skip_frames should be an Integer.")

		self.skip_frames = skip_frames


		if type(bundle_frames) is not int: 
			raise TypeError("Input Error:  bundle_frames should be an Integer.")

		self.bundle_frames = bundle_frames


	def __iter__(self):
		return self

	def next(self):

		if self.cap.isOpened()==False: 
			raise StopIteration("Input Error: Check camera number. Camera object not available")

		if self.bundle_frames == 1:
			return self.get_frame()
		else:
			return [self.get_frame() for i in xrange(self.bundle_frames)]

	def get_frame(self):

		'''
		Function 2: get_frame

		This function perfoms the following tasks:

		1. Capture frames from camera
		2. Returning frames to the calling object

		'''

		for j in xrange(self.skip_frames):
			ret,frame = self.cap.read()
			if ret==False:
				raise StopIteration("Error : Camera unable to capture frames")
				
		ret,frame=self.cap.read()

		if ret==False:
			raise StopIteration("Error : Camera unable to capture frames")

		return frame



 


if __name__ == "__main__":

	ob1=cameraArray(camera=1, skip_frames=0, bundle_frames=1)  # creating object

	for var in ob1:
		print var
		cv2.imshow("camera",var)
		k=cv2.waitKey(1)
		if k==27:
			break

	





