import numpy as np
import cv2 as cv

drawing = False # true if mouse is pressed
mode = True # if true, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1, -1

# mouse callback function
def draw_circle(event, x,y,flags,param):
	global ix,iy,drawing,mode

	if event == cv.EVENT_LBUTTONDOWN:
		drawing = True
		ix,iy = x,y

	elif event == cv.EVENT_MOUSEMOVE:
		if drawing == True:
			if mode == True:
				cv.rectangle(image,(ix,iy),(x,y),(0,255,0),-1)
			else:
				cv.circle(image,(x,y),5,(0,0,255), -1)
			cv.imshow('image', image)

	elif event == cv.EVENT_LBUTTONUP:
		drawing = False
		

image= np.zeros((512,512,3), np.uint8)
cv.imshow('image', image)
cv.setMouseCallback('image',draw_circle)

while(1):
	cv.imshow('image',image)
	k= cv.waitKey(1) & 0xff
	if k == ord('m'):
		mode = not mode
	elif k == 27 :
		break


cv.destroyAllWindows()


