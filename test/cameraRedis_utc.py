
'''-----------------------------------------------------------------------------------------------------
Provides a generator to capture frames from a camera and push to redis.
Author: Sreeram Menon
Date: 04th may 2015
Modified: 07th May 2015
Logs: N/A

Usage: 

import redis
import numpy
import cv2
import time


ob1=cameraRedis(camera=1, key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  

for var in ob1:   
	print var

	cv2.imshow('frame',var)
	
	k=cv2.waitKey(1)
	
	if k==27:
		break



-----------------------------------------------------------------------------------------------------'''
import redis
import numpy
import cv2
import time
import logging
from RedisDBoperations import Redis_Producer

'''-----------------------------------------------------------------------------------------------------

Type: Generator class
Inputs:


1. camera (Int) [defaults - 0] - The camera Number 
2. key_prefix (String) [defaults - "cam" ]- The prefix of the key
3. IP (String) [defaults - "localhost"] - IP addrress of the redis server
4. Port (Int) [defaults - 6379] - Port of the redis server
5. Password (String ) [defaults - ''] - Password of the redis server
6. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
7. bundle_frames (Int) [defaults - 1] - Number of frames to bundle when value is returned
8. wait_time (Int) [defaults - 3] - wait_time for redis consumer object creation
-----------------------------------------------------------------------------------------------------'''


class cameraRedis(object):

	def __init__(self, camera=0, key_prefix="cam", IP="localhost", Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3):

		'''
		Function 1 : __init__ (Initialisation)

		This function performs the following task:

		1. Initializes the cameraRedis class and creates an object of RedisDBoperations
		

		'''
		
		if type(IP) is not str:
			TypeError("Input Error: IP should be a String.")


		if type(Port) is not int:
			TypeError("Input Error: port should be an Integer.")


		if type(Password) is not str: 
			TypeError("Input Error:  password should be a String.")

		if type(wait_time) is not int: 
			TypeError("Input Error:  wait_time should be an Integer.")


		self.Redis_Producer_ob = Redis_Producer(host=IP, port = Port, password = Password,log_obj=log_obj,wait_time=wait_time) 



		if type(camera) is not int: 
			TypeError("Input Error:  Camera number should be an Integer.")

		self.cap = cv2.VideoCapture(camera)
		ret,frame = self.cap.read()

		if ret==False:
			TypeError("Input Error: Not able to read frames from camera. Check camerRedis.py")

		if type(skip_frames) is not int: 
			TypeError("Input Error: skip_frames should be a an integer")
		
		self.skip_frames = skip_frames
		
		if type(bundle_frames) is not int:
			TypeError("Input Error: bundle_frames should be a an integer")

		self.bundle_frames = bundle_frames

		if type(key_prefix) is not str:
			TypeError("Input Error: key_prefix should be a an integer")

		shape_key = key_prefix + "_shape" 
		self.image_key = key_prefix + "_images"
		
		self.Redis_Producer_ob.set_value(shape_key,frame.shape) # should this be changed



	def __iter__(self):
		return self

	def __next__(self):

		'''
		Function 2 : __next__

		This function perform the following tasks:

		1. Checks if video capture object is open 
		2. Bundle required number of frames 
		3. Push the resulting frame/tuple to redis

		'''

		if self.cap.isOpened()==False:
			TypeError("Input Error: Camera object not available. Check camera number and connections")

		if self.bundle_frames == 1:
			result =  self.grab_frame()
			print result.shape
			self.Redis_Producer_ob.push_value(self.image_key,result.tostring()) 

		else:
			result = [self.grab_frame() for i in xrange(self.bundle_frames)]
			self.Redis_Producer_ob.push_value(self.image_key,result.tostring())

		return result

			

	def grab_frame(self):

		'''
		Function 3 : grab_frame 

		This function perform the following task:

		1. Reads images from the camera 
		

		'''

		for j in xrange(self.skip_frames):
			ret,frame = self.cap.read()

			if ret==False: 
				raise StopIteration("Not able to read frames from camera. Check camera")

		ret,frame =self.cap.read()

		if ret==False: 
			raise StopIteration("Not able to read frames from camera. Check camera")
			
		return frame 



import unittest
import os 
from RedisDBoperations import Redis_Consumer # to check if redis has proper data 

class TestStringMethods(unittest.TestCase):

	global var 

	def test_1(self): # test if shape is a tuple and shape is the same as that of the
		Redis_Consumer_ob = Redis_Consumer(host="localhost", port = 6379, password = '',log_obj=logging.getLogger("test_logger.log"),wait_time=3) # Consumer object
		shape_obt = ast.literal_eval(Redis_Consumer_ob.get_value("camera1_shape"))
		self.assertIsInstance(shape_obt,tuple) # checks if the shape is a tuple
		self.assertEqual(shape_obt,var.shape)# checking if the shape of frames of camera is the same as that pushed to redis

	def test_2(self): # test if the consumer is able to pop out frames/tuples
		Redis_Consumer_ob = Redis_Consumer(host="localhost", port = 6379, password = '',log_obj=logging.getLogger("test_logger.log"),wait_time=3) # Consumer object
		frame_poped = Redis_Consumer_ob.pop_value("camera1_shape")) 
		self.assertFalse(frame_poped,None)

	def test_3(self): # checking camera number
		try:
			result = False
			ob1=cameraRedis(camera='s', key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_4(self): # checking key_prefix
		try:
			result = False
			ob1=cameraRedis(camera=1, key_prefix=123, IP="localhost", Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_5(self): # checking IP
		try:
			result = False
			ob1=cameraRedis(camera=1, key_prefix="camera1", IP=212, Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)


	def test_6(self): # checking Port
		try:
			result = False
			ob1=cameraRedis(camera=1, key_prefix="camera1", IP=212, Port="string", Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_7(self): # checking Password
		try:
			result = False
			ob1=cameraRedis(camera=1, key_prefix="camera1", IP=212, Port="string", Password=1, skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)


	def test_8(self): # checking skip_frames
		try:
			result = False
			ob1=cameraRedis(camera=1, key_prefix="camera1", IP=212, Port="string", Password=1, skip_frames='0', bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)


	def test_9(self): # checking bundle frames
		try:
			result = False
			ob1=cameraRedis(camera=1, Port=6379, Password='', skip_frames=1, bundle_frames='1',log_obj=logging.getLogger("test_logger.log"),wait_time=3)  
		except TypeError:
			result = True
			self.assertTrue(result)


		






		



if __name__ == "__main__":

	
	

	ob1=cameraRedis(camera=1, key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=0, bundle_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  

	for var in ob1:   
		print var

		cv2.imshow('frame',var)
		
		k=cv2.waitKey(1)
		
		if k==27:
			break


	unittest.main()
