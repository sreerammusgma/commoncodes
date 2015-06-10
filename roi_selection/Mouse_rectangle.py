import cv2
import numpy 

'''-----------------------------------------------------------------------------------------------------
Provides a method for selecting rectangles by mouseclicks and daigonal-points the coordinates of the boundary.



Author: Sreeram Menon 
Pomodoro : Venus Commmon Codes 
Date: 11 th May 2015
Modified:  14 th May 2015
Logs: N/A
---------------------------------------------------------------------------------------------------------'''




""" 
Inputs:

1. Image (numpy array) : The image from where rectangle is to be selected.
2. cordinates_rectangle (list) : The list to which coordinates will be stored and returned.


How to use:
1. Declare a list "cordinates_rectangle" where the list of coordintes is to be recorded. Call function with image and the list.
2. Doube-click two points on the image. These will be considered as daigonal points of the rectangular ROI needed.
3. Press 'l' to print the current list of selections. Press 'c' to clear last selection and 'r' to clear all selctions.
4. Press 's' to get the positions and return. Press <escape> to quit.

Note: A small circle appears at the point you select.

Usage: The python script for using this function is like this:

import cv2
import numpy

from Mouse_rectangle import * 
img = cv2.imread("/home/sreeram/Sublime/Data/v32/5.jpg") # provide an image 
cordinates_rectangle = draw_rectangle(img) # This list is the result 
print "Selected coordinates are :",cordinates_rectangle


"""



def draw_circle(event,x,y,flags,param):
    
    global ix,iy,cordinates_rectangle
    
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cordinates_rectangle.append((x,y))
        print "Last selection=",cordinates_rectangle[-1]
        cv2.circle(image,cordinates_rectangle[-1],4,(0,0,0),1)
    

    if  len(cordinates_rectangle)>1 and len(cordinates_rectangle)%2 == 0:
        cv2.rectangle(image,cordinates_rectangle[-2], cordinates_rectangle[-1], (0,255,0),3)



def mouse_rectangle(image,cordinates_rectangle):


    if image is None or type(image) is not numpy.ndarray:
        raise TypeError("The input image is not proper")

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        cv2.imshow('image',image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

        elif k == ord('l'):
            print "Selections untill now are :",cordinates_rectangle

        elif k==ord('s'):
            #print "Selected coordinates are :",cordinates_rectangle
            break
            

        elif k==ord('r'):
            print "Deleting all selections till now"
            del cordinates_rectangle[:]

        elif k==ord('c'):
            print "clearing the last selection"
            del cordinates_rectangle[-1]

    cv2.destroyAllWindows()





def draw_rectangle(img):

    global cordinates_rectangle,image
    image = img
    cordinates_rectangle = []
    mouse_rectangle(image,cordinates_rectangle)
    return cordinates_rectangle

    

if __name__=="__main__":

    img = cv2.imread("/home/sreeram/Sublime/Data/v32/4.jpg") # provide an image 
    cordinates_rectangle = draw_rectangle(img) # This list is the result 
    print "Selected coordinates are :",cordinates_rectangle


    cv2.imshow('Result',img)
    cv2.waitKey(0)


    



    
