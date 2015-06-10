
'''-----------------------------------------------------------------------------------------------------
Provides a generator to push arrays send as input to redis.
Author: Sreeram Menon
Date: 28th April 2015
Modified: 30th April 2015
Logs: N/A

Usage: 

import redis
import numpy
import cv2
import time
import logging
from RedisDBoperations import Redis_Producer

ob1=arrayRedis(frame_shape=(576,720), key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=0,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  

frame=numpy.ones((576,720))

ob1.next(frame)



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
1. frame_shape (tuple) [default - (576,720)] - The shape of the frame 
2. key_prefix (String) [default - "cam" ]- The prefix of the key
3. IP (String) [default - "localhost"] - IP addrress of the redis server
4. Port (Int) [default - 6379] - Port of the redis server
5. Password (String ) [default - ''] - Password of the redis server
6. skip_frames (Int) [default - 0] - Number of frames to skip between iterations
7. wait_time (Int) [default - 3] - wait_time for redis consumer object creation
-----------------------------------------------------------------------------------------------------'''


class arrayRedis(object):

	def __init__(self, frame_shape=(576,720), key_prefix="cam", IP="localhost", Port=6379, Password='', skip_frames=0,log_obj=logging.getLogger("test_logger.log"),wait_time=3):

		'''
		Function 1: Initialization

		1. Initializes the class, and checks the parameters.
		2. Creates an object of Redis_Producer

		'''


		if type(IP) is not str:
			raise TypeError("Input Error: IP should be a String.")


		if type(Port) is not int:
			raise TypeError("Input Error: port should be an Integer.")


		if type(Password) is not str:
			raise TypeError("Input Error:  password should be a String.")

		if type(wait_time) is not int:
			raise TypeError("Input Error:  wait_time should be an Integer.")


		self.Redis_Producer_ob = Redis_Producer(host=IP, port = Port, password = Password,log_obj=log_obj,wait_time=wait_time) 


		if type(skip_frames) is not int:
			raise TypeError("skip_frames should be a an integer")
		
		self.skip_frames = skip_frames
		self.counter = 0

		if type(key_prefix) is not str:
			raise TypeError("key_prefix should be a an integer")

		shape_key = key_prefix + "_shape" 
		self.image_key = key_prefix + "_images"

		self.Redis_Producer_ob.set_value(shape_key,frame_shape)


	def next(self,frame):

		'''
		Function 2: next

		1. Takes in the frames send my the user and writes it to redis 


		'''

		if type(frame) is not numpy.ndarray:
			raise TypeError("Frame sent for pushing to redis is not a numpy array")


		if self.counter < self.skip_frames:
			self.counter+=1
			return frame 
			
		self.Redis_Producer_ob.push_value(self.image_key,frame.tostring()) # rpush the frame 

		self.counter=0 # initilaising counter

		return frame 

			



import unittest
import os
import ast
from RedisDBoperations import Redis_Consumer 

class TestStringMethods(unittest.TestCase):

	global 	frame_shape,key_prefix, IP, Port, Password, wait_time

	def test_1(self): # test if shape is a tuple and shape is the same as that 
		ob2 = Redis_Consumer(host=host, port = Port, password = Password,log_obj=logging.getLogger("test_logger.log"),wait_time=wait_time) # Consumer object
		shape_obt = ast.literal_eval(ob2.get_value(key_prefix+"_shape"))
		self.assertIsInstance(shape_obt,tuple) #Equal(type(shape_obt),'tuple')
		self.assertEqual(shape_obt,frame_shape) # Comapring with the frame_shape

	# checking exceptional handling for the case of wrong (format) input parameters 


	def test_2(self):  # wrong frame shape

		try:
			result = False
			ob1=arrayRedis(frame_shape="wrong format")#, key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=0,log_obj=logging.getLogger("test_logger.log"),wait_time=3")  
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_3(self): # wrong key_prefix

		try:
			result = False
			ob1=arrayRedis(frame_shape=(520,340), key_prefix=124)

		except TypeError:

			result = True
			self.assertTrue(result)


	def test_4(self): # wrong IP 

		try:
			result = False
			ob1=arrayRedis(frame_shape=(512,512), key_prefix="camera1", IP=172.25)
		except TypeError:
			result = True
		
		self.assertTrue(result)

	def test_5(self): # wrong Port 

		try:
			result = False
			ob1=arrayRedis(frame_shape=(512,512),key_prefix="camera1", IP="localhost", Port="wrong port format")
		except TypeError:
			result = True
			self.assertTrue(result)


	def test_6(self): # wrong Port number

		try:
			result = False
			ob1=arrayRedis(frame_shape=(512,512),key_prefix="camera1", IP="localhost", Port="wrong port format")
		except TypeError:
			result = True
			self.assertTrue(result)


	def test_7(self): # wrong Password, password should be in string format 

		try:
			result = False
			ob1=arrayRedis(frame_shape=(576,720), key_prefix="camera1", IP="localhost", Port=6379, Password=123, skip_frames=0,log_obj=logging.getLogger("test_logger.log"),wait_time=3)
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_8(self): # wrong skip_frames

		try:
			result = False
			ob1=arrayRedis(frame_shape=(576,720), key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames='0',log_obj=logging.getLogger("test_logger.log"),wait_time=3)
		except TypeError:
			result = True
			self.assertTrue(result)

	def test_9(self): # wrong wait_time 

		try:
			result = False
			ob1=arrayRedis(frame_shape=(576,720), key_prefix="camera1", IP="localhost", Port=6379, Password='', skip_frames=1,log_obj=logging.getLogger("test_logger.log"),wait_time='should be an integer')
		except TypeError:
			result = True
			self.assertTrue(result)






if __name__ == "__main__":

	frame_shape=(576,720)
	key_prefix="camera1"
	IP="localhost"
	Port=6379
	Password=''
	wait_time=3

	
	ob1=arrayRedis(frame_shape=(576,720), key_prefix="camera1", IP="172.25.1.186", Port=6379, Password='', skip_frames=0,log_obj=logging.getLogger("test_logger.log"),wait_time=3)  

	frame=numpy.ones((576,720))

	#ob1.next(frame)


	


	unittest.main()
