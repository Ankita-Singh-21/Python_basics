import cv2
import numpy as np

def nothing(x):
    pass


frameWidth = 640
frameHeight = 360

path = '/home/ankita/Documents/Opencv/images/near_line.mp4'
#cap = cv2.VideoCapture(path);

cap = cv2.VideoCapture(0)

cap.set(3, frameWidth)
cap.set(4, frameHeight)

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

left = 0
mid = 0
right = 0


while True:
    #frame = cv2.imread('smarties.png')
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, l_b, u_b)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    #print(mask)
    #print(mask[0][0])
    #print(mask.step)
    #print(mask.size)
    print(mask.shape[0])
    #print(type(mask[1][1]))

    
    for i in range(0, (mask.shape[0] - 2) ) :
    	#print(i)
    	for j in range(0, (mask.shape[1] - 2) ) :
    		if (mask[i][j] == 0):
    			if (i > 0 and i <= 214 ):
    				left+=1
    			elif (i > 214 and i <= 428 ):
    				mid+=1
    			elif (i > 428 and i < 640 ):
    				right+=1

    if(max(left,mid,right) == left):
    	print('Left')
    if(max(left,mid,right) == mid):
    	print('Mid')
    if(max(left,mid,right) == right):
    	print('Right')
    left = 0
    mid = 0
    right = 0

    
    #cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
