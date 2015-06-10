 

'''
Provides a definition to plot pi chart, given some essential information.
Author: Sreeram Menon
Date: 08th April 2015
Modified: 08th April 2015
Logs: N/A
'''

'''-----------------------------------------------------------------------------------------------------
Name: pichart

Inputs:

1. labels (tuples) - The names of entrants into piechart
2. shares (array) - The share of each entrant
3. colors (tuples)- The color for each entrant
4. image (numpy array) [default : None ]- Image on which pichart is to be drawn. If None, the pichart will be drawn on a white image.
5. image_shape (tuples) [defaults - (512,512,3)] - Size of the image on which pi chart is drawn. Relevant only if image is None.
6. center (tuples) [defaults - ((120,256))] - Position of center of the chart
7. length_axes (tuples) [defaults- (100,100)] - Length of major and minor axes of ellipses drawn 
8. inclination (Float) [defaults - 0]- The inclinatiuon angle of the plot 
9. legend_xposition (Int) [default - 300] - The x location where legends need to appear
10.legend_yposition (Int) [default - 70] - The y location of first legend. The second one will be appear below this.
11.legend_yposition_gap (Int) [default -40]- The pixel gap between legends.

Usage:

import cv2
import numpy
from pichart import *

shares=numpy.array([10,11,27,5])
colors = ( (0,151,0), (0,0,255), (0,0,0),(0,255,125))
labels=('king','queen','ace','jack')

print len(shares),len(colors),len(labels)
image = cv2.imread('/home/sreeram/Sublime/Data/v32/6.jpg')
result = draw_piechart(labels,shares,colors,image,(512,512,3),(120,120),(100,100),0)
cv2.imshow('Pichart',result)
cv2.waitKey(0)

-----------------------------------------------------------------------------------------------------'''
import cv2
import numpy


def draw_piechart(labels,shares,colors,image=None,image_shape=(512,512,3),center=(120,120),length_axes=(100,100),inclination=0,legend_xposition=300, legend_yposition=70, legend_yposition_gap=40):

	'''
	
	Function 1: draw_piechart

	This functio performs the following tasks:

	1. This function draws a pie chart using labels, shares and colors.
	
	'''



	if len(labels)==len(shares)==len(colors):

		if type(image) is not numpy.ndarray : 

			try:
				image=255*numpy.ones(image_shape)
			except:
				image=255*numpy.ones((512,512,3))

		labels = labels
		shares =shares
		colors = colors




	else:

		raise TypeError("The lenght of labels,shares and colors are not equal.Check input...Cannot draw a pi chart..")

	

	angles = find_angles(shares)

	angles_new= numpy.zeros(len(angles)+1)

	for i in range(0,len(angles)+1):
		print i,sum(angles[0:i])
		angles_new[i]= numpy.ceil(sum(angles[0:i]))
	
		
	draw_ellipses(image,labels,shares,colors,angles,angles_new,center,length_axes,inclination,legend_xposition,legend_yposition,legend_yposition_gap)
	return image




def find_angles(shares):
	return 360*shares*0.1/(sum(shares)*0.1)


def draw_ellipses(image,labels,shares,colors,angles,angles_new, center=(120,120),length_axes=(100,100),inclination=0, legend_xposition=300, legend_yposition=70,legend_yposition_gap=40):


	
	if image is None or type(image) is not numpy.ndarray:
		image=255*numpy.ones((512,512,3))
		print "No proper background image is given by user. So pie chart will be drawn on a white background."
			
	start_angle = 0
	
	for j in range(0,len(angles)):
		
		start_angle=angles_new[j]
		end_angle=angles_new[j+1]
		cv2.ellipse(image,center, length_axes, inclination, start_angle, end_angle, colors[j],-1)
		cv2.circle(image,(legend_xposition,legend_yposition), 4, colors[j], -1)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(image,labels[j],(legend_xposition+50,legend_yposition), font, 0.5,colors[j],2)
		#cv2.putText(image,str(shares[j]),(legend_xposition+150,legend_yposition), font, 0.5,colors[j],2)
		legend_yposition+=legend_yposition_gap


			
		


		
if __name__=="__main__":

	shares=numpy.array([10,11,27,5])
	colors = ( (0,151,0), (0,0,255), (0,0,0),(0,255,125))
	labels=('king','queen','ace','jack')

	print len(shares),len(colors),len(labels)



	# Example 1 : Drawing a pie chart on a plain white image
	# Format : draw_piechart(labels,shares,colors,image=None,image_shape=(512,512,3),center=(120,120),length_axes=(100,100),inclination=0,legend_xposition=300, legend_yposition=70):

	result = draw_piechart(labels,shares,colors,None,(520,520,3),(300,250),(100,100),0,10,150,30) # 


	#print result
	cv2.imshow('Final result..',result)
	cv2.waitKey(0)

	# Example 2 : Drawing a pie chart on a given image

	image = cv2.imread('/home/sreeram/Sublime/Data/v32/5.jpg')
	result = draw_piechart(labels,shares,colors,image,(700,700,3),(200,200),(100,100),0,400,300,50)


	#print result
	cv2.imshow('Final result..',result)
	cv2.waitKey(0)



	shares=numpy.array([10,11,27,5])
	colors = ( (0,151,0), (0,0,255), (0,0,0),(0,255,125))
	labels=('king','queen','ace','jack')

	print len(shares),len(colors),len(labels)
	image = cv2.imread('/home/sreeram/Subl/Data/v32/-5.jpg')
	result = draw_piechart(labels,shares,colors,image,(512,512,3),(320,420),(100,100),0)

	cv2.imshow('Final result',result)
	cv2.waitKey(0)