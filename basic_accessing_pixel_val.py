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


left = 0
mid = 0
right = 0


while True:
    #frame = cv2.imread('smarties.png')
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    

    #cv2.imshow("frame", frame)
    dimensions = frame.shape
    print(dimensions)
    

    
    '''for i in range(0, frame.shape[1] ) :
    	for j in range(0, frame.shape[0] ) :
            print(' i', i,' j',j)
            if (i >= 0 and i < 180):
                frame[i][j] = (0,0,255)
            elif (i >= 180 and i < 359):
                frame[i][j] = (0,255,0)'''

    for i in range(0, frame.shape[0] ) :
        for j in range(0, frame.shape[1] ) :
            print(' i', i,' j',j)
            if (j >= 0 and j < 213):
                frame[i][j] = (0,0,255)
            elif (j >= 214 and j < 428):
                frame[i][j] = (0,255,0)
            


    
    #cv2.imshow("res", res)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
