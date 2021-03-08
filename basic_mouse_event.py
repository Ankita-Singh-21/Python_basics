import numpy as np
import cv2

''' print all events '''
#events = [i for i in dir(cv2) if 'EVENTS' in i]
#print(events)

''' program to listen to mouse events '''
# mouse callback function
def click_event(event, x,y, flags, param):
	'''if event == cv2.EVENT_LBUTTONDOWN:
		# print x and y coordinates
		print(x,',',y)
		font=cv2.FONT_HERSHEY_SIMPLEX
		strXY= str(x) + ',' + str(y)
		cv2.putText(img, strXY, (x,y), font, .5, (255,255,0),2)
		cv2.imshow('image', img)'''

	if event == cv2.EVENT_RBUTTONDOWN:
		# print bgr channel
		blue = img[y,x,0]
		green = img[y,x,1]
		red = img[y,x,2]
		font = cv2.FONT_HERSHEY_SIMPLEX
		strXY = str(blue) + ',' + str(green) + ',' + str(red)
		cv2.putText(img, strXY, (x,y), font, .5, (255,255,0),2)
		cv2.imshow('image', img)

	if event == cv2.EVENT_LBUTTONDOWN:
		cv2.circle(img,(x,y),3 ,(0,0,255), -1)
		points.append((x,y))
		if len(points) >=2:
			# draw lines from last two clicked points
			cv2.line(img, points[-1], points[-2],(255,0,0),5)
		cv2.imshow('image', img)
# to open black image window
img = np.zeros((512,512,3), np.uint8)
#path = '/home/ankita/Documents/Opencv/images/lena.jpeg'
#img=cv2.imread(path)
cv2.imshow('image', img)
points = []

cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
