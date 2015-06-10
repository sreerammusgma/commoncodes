
'''-----------------------------------------------------------------------------------------------------
Provides a generator to send an array of image and save it to a location.
Author: Sreeram Menon
Date: 28th April 2015
Modified: 29th April 2015
Logs: N/A

Usage: 

import numpy as np
import cv2
import os

path="/home/sreeram/Pictures/something.png" # path to store
ob1=arrayImage(path,0) 
frame = 255*np.ones((300,300,3))
ob1.next(frame)


-----------------------------------------------------------------------------------------------------'''

import numpy as np
import cv2
import os 

'''-----------------------------------------------------------------------------------------------------
Name: arrayImage
Type: Generator class
Inputs:


1. frame (numpy array) - The image in the form of array
2. destination (string) - The destination to which the array need to be stored
3. skip_frames (Int) [defaults - 0] - Number of frames to skip between iterations

-----------------------------------------------------------------------------------------------------'''


class arrayImage(object):

	def __init__(self, destination, skip_frames=0):


		'''
		Function 1: Initialisation

		1. Initilaise the class and checks for input errors 



		'''

		if os.path.exists(os.path.dirname(destination)) is False:
			TypeError("Input Error: The destination should be valid")
		

		if type(skip_frames) is not int:
			TypeError("Input Error:  skip_frames should be an Integer")



		
		self.destination = destination
		self.skip_frames = skip_frames
		self.counter=0
		



	def next(self,frame):


		'''
		Function 2: next

		1. This functions takes a numpy array and writes to image destination 

		'''


		if frame is None or (type(frame) is not numpy.ndarray):
			raise TypeError("Input Error: Frames from the folder is not of type numpy.ndarray")

		if self.counter<self.skip_frames:
			self.counter+=1
			return


		if frame is None or (type(frame) is np.ndarray)==False:
			TypeError("Frame is not proper.")



		else:
			cv2.imwrite(self.destination,frame)
			self.counter=0

		return frame 



			
		



if __name__ == "__main__":

	path="/home/sreeram/Pictures/something.png" # path to store


	ob1=arrayImage(path,0) 

	frame = 255*np.ones((300,300,3))
	
	ob1.next(frame)

	frame = 0*np.ones((400,400,3))
	
	ob1.next(frame)


	frame = 255*np.ones((500,500,3))
	
	ob1.next(frame)


	unittest.main()
