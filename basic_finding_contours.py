'''
Contours are simply a curve joining all the continuous points along a boundary
having same colour and intensity.

Contours are useful tools for shape analysis, object detection and recognition.

Main functions :
cv.findContours() , cv.drawContours()

            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

Contours is a Python list of all the contours in the image. Each individual contour
 is a Numpy array of (x,y) coordinates of boundary points of the object.

 To draw all the contours in an image:
             cv.drawContours(img, contours, -1, (0,255,0), 3)

To draw an individual contour, say 4th contour:
             cv.drawContours(img, contours, 3, (0,255,0), 3)

But most of the time, below method will be useful:
                  cnt = contours[4]
                 cv.drawContours(img, [cnt], 0, (0,255,0), 3)

'''
import numpy as np
import cv2

path = '/home/ankita/Documents/Opencv/images/vegetables.jpeg'
img = cv2.imread(path)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)

# python 2
_,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# python 3
#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print("Number of contours = " + str(len(contours)))
print(contours[0])

cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
cv2.drawContours(imgray, contours, -1, (0, 255, 0), 1)

cv2.imshow('Image', img)
cv2.imshow('Image GRAY', imgray)
cv2.waitKey(0)
cv2.destroyAllWindows()