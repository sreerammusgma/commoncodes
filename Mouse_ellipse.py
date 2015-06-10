import cv2
import numpy 


'''-----------------------------------------------------------------------------------------------------
Provides a method for selecting ellipses by mouseclicks. .



Author: Sreeram Menon 
Pomodoro : Venus Commmon Codes 
Date: 15 th May 2015
Modified:  5 th June 2015
Logs: N/A
---------------------------------------------------------------------------------------------------------'''




""" 
Inputs:

1. Image (numpy array) : The image from where ellipse is to be selected.
2. cordinates_ellipse (list) : The list to which coordinates will be stored and returned.


How to use:
1. Declare a list "cordinates_ellipse" where the list of coordintes is to be recorded. Call function with image and the list.
2. Doube-click two points on the image. These will be considered as daigonal points of the ellipse ROI needed.
3. Press 'l' to print the current list of selections. Press 'c' to clear last selection and 'r' to clear all selctions.
4. Press 's' to get the positions and return. Press <escape> to quit.

Note: A small circle appears at the point you select.

Usage: The python script for using this function is like this:

import cv2
import numpy
from Mouse_ellipse import *


img = cv2.imread("/home/sreeram/Sublime/Data/v32/5.jpg") # provide an image 
cordinates_ellipse = draw_ellipse(img) # This list is the result 
print "Selected coordinates are :",cordinates_ellipse


"""



def draw_circle(event,x,y,flags,param):
    global ix,iy,cordinates_ellipse,image 
    
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cordinates_ellipse.append((x,y))
        print "Last selection=",cordinates_ellipse[-1]
        cv2.circle(image,cordinates_ellipse[-1],4,(0,0,0),1)
    

    if  len(cordinates_ellipse)>1 and len(cordinates_ellipse)%2 == 0:
        c0=(cordinates_ellipse[-1][0]+cordinates_ellipse[-2][0])/2
        c1=(cordinates_ellipse[-1][1]+cordinates_ellipse[-2][1])/2
        d1=numpy.abs(cordinates_ellipse[-1][0]-cordinates_ellipse[-2][0])
        d2=numpy.abs(cordinates_ellipse[-1][1]-cordinates_ellipse[-2][1])
        cv2.ellipse(image,(c0,c1),(d1/2,d2/2),0,0,360,(255,0,0),2)
    




def mouse_ellipse(image,cordinates_ellipse):

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        cv2.imshow('image',image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

        elif k == ord('l'):
            print "Selections untill now are :",cordinates_ellipse

        elif k==ord('s'):

            break
            

        elif k==ord('r'):
            #print "Deleting all selections till now"
            del cordinates_ellipse[:]

        elif k==ord('c'):
            del cordinates_ellipse[-1]

    cv2.destroyAllWindows()





def draw_ellipse(img):



    if img is None or type(img) is not numpy.ndarray:
        raise TypeError("Input Error: The image is not valid")

    global cordinates_ellipse,image
    image = img
    cordinates_ellipse = []
    mouse_ellipse(image,cordinates_ellipse)
    return cordinates_ellipse

    

if __name__=="__main__":

    img = cv2.imread("/home/sreeram/Sublime/Data/v32/10.jpg") # provide an image 
    cordinates_ellipse = draw_ellipse(img) # This list is the result 
    print "Selected coordinates are :",cordinates_ellipse


    cv2.imshow('Result',img)
    cv2.waitKey(0)


    



    
