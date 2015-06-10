
'''-----------------------------------------------------------------------------------------------------
Provides a generator to make a video out of images in a given folder, stored in a serial order.
Author: Sreeram Menon
Date: 11 May  2015
Modified: 25 May 2015
Logs: N/A

Usage:

import numpy
import cv2
import os 

from folderVideo import * 

destination="/home/sreeram/Videos/video892.avi"
folderpath="/home/sreeram/Sublime/Data/v32"


ob1=folderVideo(destination,folderpath, fps=50, video_shape=(720,720), starting_index=1, ending_index=2000, prefix='', suffix=".jpg",skip_frames=1) # Creating an object of the class

for var in ob1:
	print var



-----------------------------------------------------------------------------------------------------'''

import numpy
import cv2
import os 

'''-----------------------------------------------------------------------------------------------------
Name: folderVideo
Type: Generator class
Inputs:



1. destination (string) - The path where video is to be stored.
2. folder_path (string) - The folder where frames are stored

The image files should be named serially, like 1.jpg,2.jpg and so on, however, they can have prefixes and suffixes
Ex: If names are like image_1_new.jpg,image_2_new.jpg etc. put prefix as "image_" and suffix as "_new.jpg"

3. prefix (string) [default -""]- The prefix to the name of the image index
4. suffix (string) [default-".jpg"]- the suffix to the name of image index

5. starting_index (Int) [default-1]- The index of the first image
6. ending_index (Int) [default-100]- The index of the last image 

So in the above example : image_1_new.jpg to image_100_new.jpg will be written to the video 

7. skip_frames (Int) [defaults - 0] - Number of frames to skip in between

-----------------------------------------------------------------------------------------------------'''


class folderVideo(object):

	def __init__(self, destination, folder_path, fps=20, video_shape=(480,640),starting_index=1, ending_index=100, prefix="", suffix=".jpg",skip_frames=0):

		'''
		Definition 1: Initialization

		This function perfoms the following tasks:

		1. Creates an object of the class
		2. Creates a video-writer object and writes the frame ti the video 

		'''

		if os.path.exists(os.path.dirname(destination)) is False:
			raise TypeError("Input Error: The destination should be valid")

		self.destination = destination

		if os.path.exists(folder_path) is False: 
			raise TypeError("Input Error: The destination should be valid")
		
		self.folder_path = folder_path

		if type(starting_index) is not int : 
			raise TypeError("Input Error: The starting index is not an integer")

		self.starting_index =starting_index
		
		if type(ending_index) is not int : 
			raise TypeError("Input Error: The ending index is not an integer")

		self.ending_index = ending_index

		if type(prefix) is not str: 
			raise TypeError("Input Error: prefix should be a string")

		self.prefix = prefix

		if type(suffix) is not str: 
			raise TypeError("Input Error: suffix should be a string")

		self.suffix = suffix

		if type(skip_frames) is not int:
			raise TypeError("Input Error: skip_frames should be an integer")

		self.skip_frames = skip_frames

		if type(video_shape) is not tuple:
			TypeError("Input Error: video_shape is not a tuple. Continuing with video_shape=(480,640)")
			self.video_shape=(480,640)

		else:
			self.video_shape = video_shape

		if type(fps) is not int or fps<=0:
			TypeError("fps must be a positive integer, we are proceeding with fps=20")
			fps=20


		fourcc = cv2.cv.CV_FOURCC('X','V','I','D')

		self.out = cv2.VideoWriter(self.destination,fourcc, fps, self.video_shape)

		self.index=starting_index
		self.counter=0

	
	def __iter__(self):
		return self


	def __next__(self):
		return self.next()

	def next(self):

		'''
		Function 2 :  next

		This function perfoms the following tasks:

		1. Reads the frame in a serial manner and writes to the video 

		'''

		if self.index>self.ending_index:

			self.out.release()
			raise StopIteration("Image index exceeded ending_index. Video writing ends.")

		self.index+=1
		
		if self.counter<self.skip_frames:
			self.counter+=1
			return
		
		self.counter=0


		frame = cv2.imread(self.folder_path+"/"+self.prefix+str(self.index)+self.suffix)


		if frame is None or (type(frame) is not numpy.ndarray):
			raise StopIteration("Frames from the folder is not of type numpy.ndarray")
			


		frame=cv2.resize(frame,self.video_shape)
		
		self.out.write(frame)   
		
		


		return frame 
		

if __name__ == "__main__":

	destination="/home/sreeram/Videos/video9999.avi"
	folder_path="/home/sreeram/Sublime/Data/v32"
	

	ob1=folderVideo(destination=destination,folder_path=folder_path, fps=50, video_shape=(640,480), starting_index=1, ending_index=2000, prefix='', suffix=".jpg",skip_frames=0)

	for var in ob1:
		print var 
		cv2.imshow('',var)
		h=cv2.waitKey(1)
		if h==27:
			break


	





		
