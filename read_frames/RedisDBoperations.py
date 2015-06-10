import redis
import time
import logging
import numpy as np
import ast
import cv2
import random
import json




'''-----------------------------------------------------------------------------------------------------
Provides a class for data-base (db) operations for Redis.
The objects of the class perform various db operations. 


Author: Sreeram Menon 
Pomodoro : Venus Commmon Codes 
Date: 4th may 2015
Modified: 15th may 2015
Logs: N/A

Usage: 

Redis_object = Redis_operations(host = "localhost", port = 6379, password = '', log_obj = logging.getLogger("test_logger"))

Redis_object.<db operation>(parameters)

Note: The names of similar dB operations are same for Redis and kafka (see kafkaDBoperations).

'''

'''

Class parameters:

1. host (String) - Prefix for the shape and images keys in redis
3. port (Int) [defaults - 6379] - Port of the redis server
4. password (String / None) [defaults - ''] - Password of the redis server
4. Logger 
5. wait_time (Int) [defaults - 3] - Wait in ms for next frame in case redis queue is empty

The db Operations included in the classes are:

A. Redis_Producer


A.1 msg_length : Returns the length of the list stored at key

	Parameters: 1. input_key <Redis key: typically strings>

	Usage : <Redis_Producer object>.msg_length(<input_key>)

A.2 push_value : Pushes the meassage-key pair to redis

	Parameters: 1. input_key, 2. input_message <list/string/Int/array/tuples etc..>

	Usage : <Redis_Producer object>.push_value(<input_key>,<input_message>)

A.3 set_value : Sets a value to the key 
	
	Parameters: 1. input_key, 2. value   

	Usage : <Redis_Producer object>.set_value(<input_key>,<value>)


B. Redis_Consumer


B.1 delete_msg : Delets the message corresponding to the key

	Parameters: 1. input_key

	Usage : <Redis_Consumer object>.delete_msg(<input_key>)

B.2 get_value : Pops out the message pushed to the given key 

	Parameters: 1. input_key 

	Usage : <Redis_Consumer object>.get_value(<input_key>)

B.3 pop_value :  Removes and returns the first element of the list stored at key.

	Parameters: 1. input_key

	Usage : <Redis_Consumer object>.pop_value(<input_key>)


B.4 check_key_value : Checks the existance of a key in the database
	
	Parameters: 1. input_key, 2. message_type 3. data_type (datatype) [default: 'uint8'], 4. mode (default : None)

	Usage : <Redis_Consumer object>.check_key_value(<input_key>,<message_type>,<data_type>,<mode>)



-----------------------------------------------------------------------------------------------------'''





class Redis_Producer(object):

	def __init__(self, host = "localhost", port = 6379, password = '', log_obj = logging.getLogger("test_logger.log"),wait_time=3):


		
		
		self.R = redis.Redis(host, port, password)
		
		self.log_obj = log_obj
		#self.log_obj.info("logged into redis")
		#print self.log_obj

		while self.R is None:
			print "Redis not getting connected...Trying for Connection....."
			time.sleep(wait_time)
			self.R = redis.Redis(host, port, password)

		print "Connected to Redis:", "Host:",host,"Port:",port



		
	# def make_connection(self,host = "localhost", port = 6379, password = '', log_obj = logging.getLogger("test_logger")):

	# 	'''
	# 	Function : Establish Redis connection 
	''' (The function to make connection is removed as per instructions given to the Author) '''

	# 	'''



	# 	self.R = redis.Redis(self.host, self.port, self.password)

		
	# 	if self.R != "None":
	# 		self.log_obj.info("Connection has been created")
	# 		self.log_obj.debug("Number of connections " + str(connection_count))		
		
	# 	else:
	# 		self.log_obj.error("Connection Failed")
	# 		exit()



	

		

	def delete_key(self,input_key):

		'''Function : Removes the specified keys. A key is ignored if it does not exist.'''
		
		if self.R is None:
			
			#self.R = self.make_connection()
			print "Check Redis Connection"
		
		self.R.delete(input_key)	

		self.log_obj.info("Deleted " + input_key)


	def push_value(self,  input_key, input_message):


		""" Function : Insert the message at the tail of the list stored at key"""

		if self.R  is None:

			#self.R = self.make_connection()
			print "Check Redis Connection"

		#Exception Handling
		try:
			self.R.rpush(input_key, input_message)

		except redis.exceptions.ResponseError as response:
			self.log_obj.error(response)
			exit()

	
	#Sets a value to a key 
	def set_value(self, input_key,input_message):

		"""

		Function:

		Set key to hold the string value. If key already holds a value, 
		it is overwritten, regardless of its type

		"""
	
		if self.R is  None:
			#self.R = self.make_connection()
			print "Check Redis Connection"

		
		
		#Exception Handling
		try:
			self.R.set(input_key, input_message)
		except redis.exceptions.ResponseError as response:
			self.log_obj.error(response)
			exit()


	
	

class Redis_Consumer(object):


	def __init__(self, host = "localhost", port = 6379, password = '', log_obj = logging.getLogger("test_logger.log"),wait_time=3):


		
		
		self.R = redis.Redis(host, port, password)

		self.log_obj = log_obj
		# self.log_obj.basicConfig(filename='/home/sreeram/Sublime/example.log')
		# self.log_obj.info("logged into redis")
		

		while self.R is None:
			print "Redis not getting connected...Trying for Connection....."
			time.sleep(wait_time)
			self.R = redis.Redis(host, port, password)

		print "Connected to Redis: ", "Host:",host,"Port:",port


	def msg_length(self, input_key):


		'''
		
		Function : 
		
		Returns the length of the list stored at key. If key does not exist, 
		it is interpreted as an empty list and 0 is returned. 
		An error is returned when the value stored at key is not a list.

		'''
		

		

		try:
			
			return self.R.llen(input_key)
			
		
		except redis.exceptions.ResponseError as response:
			
			self.log_obj.error(response)
			exit()

		





	def get_value(self, input_key):

		"""

		Function:

		Get the value of key. If the key does not exist the special value nil is returned. 
		An error is returned if the value stored at key is not a string, because GET only handles string values.

		"""
	
		if self.R is None:
			#self.R = self.make_connection()
			print "Check Redis Connection"

		
		
		#Exception Handling
		try:
			
			print "Getting value of the input key"
			return self.R.get(input_key)
		except redis.exceptions.ResponseError as response:
			self.log_obj.error(response)
			

	#Pops a message from a message queue
	def pop_value(self, input_key):

		"""

		Function:

		Removes and returns the first element of the list stored at key.

  		"""

		if self.R is None:
			#self.R = self.make_connection()
			print "Check Redis Connection"

		self.input_key = input_key
		
		#Exception Handling
		try:
			self.output = self.R.lpop(input_key)
		except redis.exceptions.ResponseError as response:
			self.log_obj.error(response)
			exit()
		
		return self.output

	def check_key_value(self, input_key, message_type="numpy", data_type = 'uint8', mode = None):


		
		"""Function : Checks the existence of key in database"""

		if self.R is None:
			#self.R = self.make_connection() 
			print "Check Redis Connection"


		while True:

			if message_type != "ast":
				self.key_len = 0
				while self.key_len < 1:
					self.key_len = self.msg_length(input_key)
					if mode == "Display":
						self.log_obj.debug("waiting for "+input_key)
					time.sleep(0.01)
			else:
				while self.pop_value(input_key) == None:
					if mode == "Display":
						self.log_obj.debug("waiting for "+input_key)

					time.sleep(0.01)

			if message_type == "numpy":
				return np.fromstring(self.pop_value(input_key), dtype = data_type)

			elif message_type == "string":
				return self.pop_value(input_key)

			elif message_type == "json":
				return json.loads(self.pop_value(input_key))

			elif message_type == "ast":
				return ast.literal_eval(self.pop_value(input_key))
			else:
				self.log_obj.error("Wrong data in variable message type")
				exit()

	def delete_key(self,input_key):

		'''Function : Removes the specified keys. A key is ignored if it does not exist.'''
		
		if self.R is None:
			
			#self.R = self.make_connection()
			print "Check Redis Connection"
		
		self.R.delete(input_key)	

		self.log_obj.info("Deleted " + input_key)


			

import unittest
import os

class TestStringMethods(unittest.TestCase):

	global Redis_Producer_ob, Redis_Consumer_ob 

	def test_1(self): # checking the existence of Producer object
		print "test1"
		self.assertTrue(Redis_Producer_ob is not(None))
		
	def test_2(self): #  checking the existence of Producer object
		print "test2"
		self.assertTrue(Redis_Consumer_ob is not(None))

	def test_3(self): # pushing a value to a key, popping it out and checking for similarity
		print "test3"
		Redis_Producer_ob.push_value("keyyy","unittest")
		self.assertEqual(  Redis_Consumer_ob.pop_value("keyyy") , "unittest" )

	def test_4(self): # setting a value to a key, getting it, and comparing
		print "test4"
		Redis_Producer_ob.set_value("key_set","The key set")
		self.assertEqual(Redis_Consumer_ob.get_value("key_set"),"The key set")


	def test_5(self): # deleting a key and ensuring that values are deleted
		print "test5"
		Redis_Producer_ob.delete_key("key_set")
		self.assertEqual(Redis_Consumer_ob.get_value("key_set"),None)



	def test_6(self): # checking the length of the message
		print "test6"
		Redis_Producer_ob.push_value("key_push","1")
		Redis_Producer_ob.push_value("key_push","2")
		print "message length is",Redis_Consumer_ob.msg_length("key_push")

		expected_length=16 # HAVE TO BE CHANGED, AND PUT FLAG==True fo this checking to happen
		FLAG=False # True

		if FLAG==True:
			self.assertEqual(Redis_Consumer_ob.msg_length("key_push"),expected_length)
				
		Redis_Consumer_ob.pop_value("key_push") 
		Redis_Consumer_ob.pop_value("key_push")


if __name__=="__main__":

	Redis_Producer_ob = Redis_Producer(host="localhost", port = 6379, password = '',log_obj=logging.getLogger("test_logger.log"),wait_time=3) # Producer object
	Redis_Consumer_ob = Redis_Consumer(host="localhost", port = 6379, password = '',log_obj=logging.getLogger("test_logger.log"),wait_time=3) # Consumer object
	




	Redis_Producer_ob.push_value("keyz222","storm")
	print "The value popped out is",Redis_Producer_ob.push_value("keyz2",('hai'))
	print "The lenght of message in the key is",Redis_Consumer_ob.msg_length("keyz2")



	Redis_Producer_ob.set_value("hello",30)
	print "The value in the key is",Redis_Consumer_ob.get_value("hello")
	print "Result of check key value is ",Redis_Consumer_ob.check_key_value("keyz222","string","uint8","Display")

	unittest.main()
	




















