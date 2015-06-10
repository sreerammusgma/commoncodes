
'''-----------------------------------------------------------------------------------------------------
Provides a generator to receive frames (numpy array from an algorithm), and write it to video file 
Author: Sreeram Menon
Date: 28th April 2015
Modified: 29 th April 2015
Logs: N/A

Usage:



import numpy
import cv2
import os
from arrayVideo import *

destination="/home/sreeram/Videos/video9190.avi"
fps=25
video_shape=(500,500)
ob1=arrayVideo(destination,fps,video_shape,skip_frames=0) # Creating an object of the class

framepath="/home/sreeram/Sublime/Data/v32/"
count=1

while True:
	
	filepath=framepath+str(count)+'.jpg'
	print filepath
	frame=cv2.imread(filepath)
	

	if frame is None:
		break
	
	print count 
	ob1.next(frame)
	cv2.imshow('',frame)
	k=cv2.waitKey(2)
	if k==27:
		break 

	count+=1 


ob1.out.release()




# See example below

-----------------------------------------------------------------------------------------------------'''

import numpy
import cv2
import os


'''-----------------------------------------------------------------------------------------------------
Name: cameraFile
Type: Generator class
Inputs:


1. destination (string) - The destination of the frame from camera
2. fps (Int) [defaults- 20]- The number of frames per second in the video
3. video_shape (Tuple) [default - (640,480)] - The shape of the video frame 
4. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
5. frame (numpy array) - The frame to be written to video 
-----------------------------------------------------------------------------------------------------'''


class arrayVideo(object):

	def __init__(self, destination, fps=20, video_shape=(480,640), skip_frames=0):

		'''

		Function 1 : Initialization 

		Parameters:
		
		1. destination 
		2. fps
		3. video_shape
		4. skip_frames

		This function performs the following:

		1. Checks and sets the values of the parameters 

		2. Initialise the video writer object



		'''

		if type(fps) is not int:
			raise TypeError("Input Error:  fps should be an Integer")

		if type(video_shape) is not tuple:
			raise TypeError("Input Error:  video_shape should be a tuple")

		self.video_shape = video_shape

		if os.path.exists(os.path.dirname(destination)) is False:
			raise TypeError("Input Error: The destination should be valid")

		

		fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
		self.out = cv2.VideoWriter(destination,fourcc, fps, video_shape) # should it be put as global so that out. release can be done.
		

		if type(skip_frames) is not int :
			raise TypeError("Input Error:  skip_frames should be a tuple")

		self.skip_frames = skip_frames

		self.counter=0 # counter is to count the number of frames skipped
 
	

	def __next__(self):
		return self.next()

	def next(self,frame):

		'''

		Function 2 : next

		Parameters :

		1. frame : Input frame to be written to video 

		This functio performs the following :

		1. checks the validity of the frame, skips required number of frames 

		2. reshape the frame to the specified shape, and writes the frame 

		'''

		if self.counter<self.skip_frames:
			self.counter+=1
			return 
		

		if frame is None or type(frame) is not numpy.ndarray:
			raise StopIteration("Wrong input frame sent for writing video. The frame sent is not numpy.ndarray")

		frame=cv2.resize(frame,self.video_shape) # resizing the frame 
		
		self.out.write(frame) # writing the frame to the video
		
		self.counter=0 # reset the counter once a frame is written to the video

		return frame 
		

import unittest
import os

class TestStringMethods(unittest.TestCase):

	global ob1,destination

	def test_1(self): # test if shape is a tuple and shape is the same as 
		print "test1"
		shape_obt = ast.literal_eval(ob1.connection.get("Rediskeyz_shape"))
		print "shape obtained...",shape_obt
		self.assertIsInstance(shape_obt,tuple) #Equal(type(shape_obt),'tuple')
		self.assertEqual(shape_obt,video_shape)


	def test_2(self): # test if the image is stored in the destination 
		self.assertTrue(  (frame==frame2).all() )




if __name__ == "__main__":

	destination="/home/sreeram/Videos/video9190.avi"
	fps=25
	video_shape=(500,500)
	ob1=arrayVideo(destination,fps,video_shape,skip_frames=0) # Creating an object of the class

	framepath="/home/sreeram/Sublime/Data/v32/"
	count=1

	while True:
		
		filepath=framepath+str(count)+'.jpg'
		print filepath
		frame=cv2.imread(filepath)
		

		if frame is None:
			break
		
		print count 
		ob1.next(frame)
		cv2.imshow('',frame)
		k=cv2.waitKey(2)
		if k==27:
			break 

		count+=1 

	
	ob1.out.release()

	




		
