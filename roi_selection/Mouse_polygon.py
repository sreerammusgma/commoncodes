import cv2
import numpy 


'''-----------------------------------------------------------------------------------------------------
Provides a method for selecting a polygon by mouseclicks and returning the coordinates of the boundary.



Author: Sreeram Menon 
Pomodoro : Venus Commmon Codes 
Date: 14th May 2015
Modified: 18th May 2015
Logs: N/A
---------------------------------------------------------------------------------------------------------'''




""" 
Inputs:

1. Image (numpy array) : The image from where polygon is to be selected.
2. cordinates_polygon (list) : The list to which coordinates will be stored and returned.


How to use:
1. Declare a list "cordinates_polygon" where the list of coordintes is to be recorded. Call function with image and the list.
2. Doube-click two points on the image. These will be considered as daigonal points of the rectangular ROI needed.
3. Selections will be displayed. Press 'l' to see the current list of points.
4. Press 's' to get the positions and return. Press <escape> twice to quit.

Usage: The python script for using this function is like this:

import cv2
import numpy
from Mouse_polygon import * 

img = cv2.imread("/home/sreeram/Sublime/Data/v32/5.jpg") # provide an image 
cordinates_polygon = draw_polygon(img) # This list is the result 
print "Selected coordinates are :",cordinates_polygon


"""



def draw_circle(event,x,y,flags,param):
    global ix,iy,cordinates_polygon
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cordinates_polygon.append((x,y))
    if len(cordinates_polygon)>1:
        #print cordinates_polygon[-1],cordinates_polygon[-2]
        cv2.line(image,cordinates_polygon[-1],cordinates_polygon[-2],(255,0,0),4)


def mouse_polygon(image,cordinates_polygon):

    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)

    while(1):
        cv2.imshow('image',image)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

        elif k == ord('l'):
            print "Selections untill now are :",cordinates_polygon

        elif k==ord('s'):
            #print "Selected coordinates are :",cordinates_polygon
            return 
            

        elif k==ord('r'):
            print "Deleting cordinates_polygon..."
            del cordinates_polygon[:]
    cv2.destroyAllWindows()





def draw_polygon(img):

    if img is None or type(img) is not numpy.ndarray:
        raise TypeError("Input Error: The input image is not proper")

    global cordinates_polygon,image
    image = img
    cordinates_polygon = []
    mouse_polygon(image,cordinates_polygon)
    return cordinates_polygon

    

if __name__=="__main__":

    img = cv2.imread("/home/sreeram/Sublime/Data/v32/5.jpg") # provide an image 
    cordinates_polygon = draw_polygon(img) # This list is the result 
    print "Selected coordinates are :",cordinates_polygon

    print "over"

    for j in range(0,len(cordinates_polygon)-1):
        cv2.line(img,cordinates_polygon[j],cordinates_polygon[j+1],(0,255,0),4)

    cv2.imshow('Result',img)
    cv2.waitKey(0)


    



    
