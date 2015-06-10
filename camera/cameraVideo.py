
'''-----------------------------------------------------------------------------------------------------
Provides a generator to capture images from a camera and store it as a video. 
Author: Sreeram Menon
Date: 04th May 2015
Modified: 04th May 2015
Logs: N/A

Usage: 

import numpy
import cv2
import os
from cameraVideo import *

# Make sure that a camera is connected to the system

ob1=cameraVideo(camera=1,destination="/home/sreeram/videopqr.avi",fps=20, video_shape=(480,640), skip_frames=0)

for var in ob1:
	print var
	cv2.imshow('camera frames',var)
	k=cv2.waitKey(1)
	if k==27:
		break

ob1.out.release()



-----------------------------------------------------------------------------------------------------'''


'''-----------------------------------------------------------------------------------------------------
Name: cameraVideo
Type: Generator class


Inputs:

1. destination (string) - The destination of the video made out of frames from camera.....for example : "/path/something.avi"
2. camera (Int) [defaults - 0] - The camera Number
3. fps (Int) [defaults - 20] - Frames per second
4. video_shape[ defaults - (480,640)] - The shape of the frames in video 
5. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
-----------------------------------------------------------------------------------------------------'''


class cameraVideo(object):

	def __init__(self, destination, camera=0, fps=20, video_shape=(480,640), skip_frames=0):


		'''
		Function 1 : __init__ (Initialisation)

		This function performs the following task:

		1. Initializes the cameraRedis class and creates an object of RedisDBoperations.
		2. A video writer object with given specifications is created.
		

		'''

		if type(camera) is not int:
			raise TypeError("Input Error:  camera(number) should be an Integer")

		self.cap = cv2.VideoCapture(camera)

		if self.cap.isOpened()==False:  
			raise TypeError("Input Error:  camera object is not created. Check camera number and settings")


		if type(fps) is not int or fps<=0 :
			raise TypeError( "Input Error:  fps should be a positive Integer")

		if type(video_shape) is not tuple:
			raise TypeError("Input Error:  video_shape should be a tuple")

		self.video_shape = video_shape

		if type(skip_frames) is not int:
			raise TypeError("Input Error:  skip_frames should be an intrger")

		self.skip_frames = skip_frames

		if os.path.exists(os.path.dirname(destination)) is False: 
			raise TypeError("Input Error: destination should be valid")

		fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
		self.out = cv2.VideoWriter(destination,fourcc, fps, self.video_shape) # should it be put as global so that out. release can be done.

		

	def __iter__(self):
		return self

	def next(self):

		'''
		Function 2: next

		This function performs the following task:

		1. Grabs frames from the camera and writes to the video. 

		'''


		if self.cap.isOpened()==False: 
			raise StopIteration("Error. Check camera number. Camera object not available")

		for j in xrange(self.skip_frames):
			ret,frame = self.cap.read()
			if ret==False: 
				raise StopIteration("No frames from camera. Check camera")
		
		ret,frame=self.cap.read()

		if ret==False: 
			raise StopIteration("No frames from camera. Check camera")

		frame = cv2.resize(frame,self.video_shape) 
		print frame.shape
		self.out.write(frame)
		return frame




import numpy
import cv2
import os 		

		
if __name__ == "__main__":

	camera = 2
	destination = "/home/sreeram/videopqr.avi"
	video_shape =(640,480)
	skip_frames=0

	ob1=cameraVideo(destination=destination,camera=camera, fps=20,video_shape=video_shape,skip_frames=skip_frames)


	for var in ob1:
		print var.shape
		cv2.imshow('camera frames',var)
		k=cv2.waitKey(1)
		if k==27:
			break


	ob1.cap.release()

	
