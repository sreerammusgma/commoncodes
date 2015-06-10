
'''-----------------------------------------------------------------------------------------------------
Provides a generator to recieve frames from redis, given the connection details and key prefix, and write them to a video.
Author: Sreeram 
Date: 11th May 2015
Modified: 25th May 2015
Logs: N/A

Usage: 

#1.Befor using this file, mmke sure redis has frames needed for writing are present with proper keys, else nothing will pop-out 
#2.Use the same key in the code

from redisVideo import *
from RedisDBoperations import Redis_Consumer
import redis
import numpy
import ast
import cv2
import logging
import os

destination="/home/sreeram/Videos/redis_video.avi"

ob1=redisVideo(destination="/home/sreeram/Videos/redis_videopqr.avi",key_prefix="Grosjean", IP="localhost", port=6379, password='', wait_time=30, skip_frames=0,log_obj = logging.getLogger("test_logger.log"))

for var in ob1:
	print var

ob1.out.release()




-----------------------------------------------------------------------------------------------------'''

import redis
import numpy
import ast
import cv2
from RedisDBoperations import Redis_Consumer
import logging
import os

'''-----------------------------------------------------------------------------------------------------
Name: redisVideo
Type: Generator class
Inputs:
1. destination (string) - the path to the video file
2. fps (Int) [defaults - 20] - The number of frames per second
3. video_shape (tuple)(default - (480,640)) - The shape of the video frame
4. key_prefix (String) - Prefix for the shape and images keys in redis
5. IP (String) [defaults - "localhost"] - IP addrress of the redis server
6. port (Int) [defaults - 6379] - Port of the redis server
7. password (String ) [defaults - ''] - Password of the redis server
8. wait_time (Int) [defaults - 30] - Wait in ms for next frame in case redis queue is empty
9. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations
10. log_obj (logger)  [defaults - "test_logger.log"] - The logger file 
-----------------------------------------------------------------------------------------------------'''


class redisVideo(object):

	def __init__(self, destination, fps=20, video_shape=(480,640), key_prefix="cam", IP="localhost", port=6379, password='',wait_time=30, skip_frames=0,log_obj = logging.getLogger("test_logger.log")):
		
		'''
		Function 1 : Initialisation

		1. Initialise Redis connection
		2. Create keys for image and shape 
		3. Create video writer object

		'''


		if type(IP) is not str:
			TypeError("Input Error: IP should be a String.")


		if type(port) is not int:
			TypeError("Input Error: port should be an Integer.")


		if type(password) is not str: 
			TypeError("Input Error:  password should be a String.")

		if type(wait_time) is not int:
			TypeError("Input Error:  wait_time should be an Integer.")


		self.Redis_Consumer_ob = Redis_Consumer(IP, port, password, log_obj,wait_time) # Consumer object

		if type(skip_frames) is not int:
			TypeError("Input Error:  skip_frames should be an Integer.")


		self.skip_frames = skip_frames


		if type(key_prefix) is not str:
			TypeError("Input Error: key_prefix should be a string.")


		shape_key = key_prefix + "_shape"  # shape_key for getting the shape of the frame
		self.image_key = key_prefix + "_images" 
		
		self.frame_shape = ast.literal_eval(self.Redis_Consumer_ob.get_value(shape_key)) # getting the shape of the frames in redis
		

		if type(self.frame_shape) is not tuple:
			TypeError("frame_shape should be a tuple")

		

		if type(fps) is not int:
			TypeError("Input Error:  fps should be an Integer.")

		if type(video_shape) is not tuple:
			TypeError("Input Error:  video_shape should be a tuple")

		self.video_shape = video_shape

		if os.path.exists(os.path.dirname(destination)) is False:
			TypeError("Input Error: The destination should be valid")

		fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
		
		self.out = cv2.VideoWriter(destination,fourcc, fps, self.video_shape) # should it be put as global so that out. release can be done. 

		


	def __iter__(self):
		return self

	def next(self):

		'''
		Function 2 :

		1. Pops out strings  from redis 

		2. Reshape the strings to image, based on the shape obtained using shape_key

		3. Reshape the frame to the size needed for video 

		4. Write the reshaped frame to the video 

		'''


		for j in xrange(self.skip_frames):
			frame_string = self.Redis_Consumer_ob.pop_value(self.image_key)
			

		frame_string = self.Redis_Consumer_ob.pop_value(self.image_key)

		if frame_string is None:
			raise StopIteration

		frame_flat_array = numpy.fromstring(frame_string,dtype=numpy.uint8)
		frame=numpy.reshape(frame_flat_array,self.frame_shape)
		frame = cv2.resize(frame,self.video_shape) 
		
		self.out.write(frame)
		return frame





if __name__=="__main__":

	ob1=redisVideo(destination="/home/sreeram/Videos/redis_videoxyz.avi",key_prefix="Grosjean", IP="localhost", port=6379, password='', wait_time=30, skip_frames=0,log_obj = logging.getLogger("test_logger.log"))

	for var in ob1:
		print var

	ob1.out.release()

	
