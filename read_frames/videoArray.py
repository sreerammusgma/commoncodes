
'''-----------------------------------------------------------------------------------------------------
Provides a generator to extract frames from a video and return them as numpy array.
Author: Sreeram Menon
Date: 28th April 2015
Modified: 8th June 2015
Logs: N/A

Usage: 

import numpy
import cv2


path = "/home/sreeram/Sublime/Data/Sample Lap GRO_OB_1.53.597_Graphic.mpg" 
# Put a valid path (String)  


object1 = videoArray(path, skip_frames=0, bundle_frames=1)

for var in object1:
	print var 


-----------------------------------------------------------------------------------------------------'''

import numpy
import cv2 

'''-----------------------------------------------------------------------------------------------------

Type: Generator class
Inputs:


1. path (string)- Path to the video
2. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
3. bundle_frames (int) [defaults - 1] - Number of frames to bundle when value is returned
-----------------------------------------------------------------------------------------------------'''


class videoArray(object):

	def __init__(self, path, skip_frames=0, bundle_frames=1):

		
		if os.path.exists(os.path.dirname(path)) is False:
			raise TypeError("Input Error: The destination should be valid")

		if type(skip_frames) is not int:
			raise TypeError("Input Error:  skip_frames should be an Integer")

		self.skip_frames = skip_frames

		if type(bundle_frames) is not int:
			raise TypeError("Input Error:  bundle_frames should be an Integer")
		
		self.bundle_frames = bundle_frames

		self.cap = cv2.VideoCapture(path)

		if self.cap.isOpened() is False:
			raise TypeError("Input Error: Unable to open video")



	def __iter__(self):
		return self

	def next(self):

		if self.bundle_frames == 1:
			return self.get_frame()
		else:
			return [self.get_frame() for i in xrange(self.bundle_frames)]

	def get_frame(self):

		for j in xrange(self.skip_frames):
			ret,frame = self.cap.read()
			if ret == False:
				raise StopIteration("Frames cannot be read from the video. Either video does not exist or Frames are over")


		ret,frame = self.cap.read()

		if ret == False:
			raise StopIteration("Frames cannot be read from the video. Either video does not exist or Frames are over")

		return frame



import unittest
import os

class TestStringMethods(unittest.TestCase):

	global path,var 

	def test_1(self): # checking the type of data returned from video
		self.assertIsInstance(var,numpy.ndarray)
		


	def test_2(self): #  comparing the shapes of video and frames returned
		cap=cv2.VideoCapture(path)
		_,fr=cap.read()
		self.assertEqual(fr.shape,var.shape)

	# Checking exception handling  

	def test_3(self):# wrong video-path
		try:
			result = False
			ob1=videoArray(path="/home/sreeram/Videos/wrongvideo.avi",skip_frames=0,bundle_frames=1)  
		except TypeError:
			result = True
		self.assertTrue(result)


	def test_4(self):# wrong skip_frames
		try:
			result = False
			ob1=videoArray(path="/home/sreeram/Sublime/Data/Sample Lap GRO_OB_1.53.597_Graphic.mpg",skip_frames='s') 
		except TypeError:
			result = True
		self.assertTrue(result)

	def test_5(self):# wrong bundle_frames
		try:
			result = False
			ob1=videoArray(path="/home/sreeram/Sublime/Data/Sample Lap GRO_OB_1.53.597_Graphic.mpg",skip_frames=1,bundle_frames='s') 
		except TypeError:
			result = True
		self.assertTrue(result)




		


if __name__=="__main__":

	path="/home/sreeram/Sublime/Data/Sample Lap GRO_OB_1.53.597_Graphic.mpg" # path to the video
	skip_frames=1
	bundle_frames=1

	ob1=videoArray(path,skip_frames,bundle_frames)  # here one frame will be skipped  


	for var in ob1:
		print var # the result 
		# the remaining is for illustration....imshow will fail if bundling is done.
		if bundle_frames == 1:
			cv2.imshow('',var)
			k=cv2.waitKey(1) 
			if k==27:
				break

	
