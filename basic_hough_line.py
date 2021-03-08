import cv2
import numpy as np 

path='/home/ankita/Documents/Opencv/images/drone_capture.jpg'

img= cv2.imread(path)
img=cv2.resize(img, (640,360))

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel2 = np.ones((5,5),np.uint8)
erosion = cv2.dilate(gray,kernel2,iterations = 3)
edges = cv2.Canny(erosion,60,70,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180, 100)

if lines is not None:
                for r,theta in lines[1]:
                    print('check')

                # Stores the value of cos(theta) in a
                    a = np.cos(theta)

                # Stores the value of sin(theta) in b
                    b = np.sin(theta)

                # x0 stores the value rcos(theta)
                    x0 = a*r

                # y0 stores the value rsin(theta)
                    y0 = b*r

                # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
                    x1 = int(x0 + 1000*(-b))

                # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
                    y1 = int(y0 + 1000*(a))

                # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
                    x2 = int(x0 - 1000*(-b))

                # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
                    y2 = int(y0 - 1000*(a))

                    cv2.line(img,(x1,y1), (x2,y2), (255,0,0),5)

cv2.imshow("image1" , img)
cv2.imshow("image2" , gray)
cv2.imshow("image3" , erosion)
cv2.imshow("image4" , edges)

cv2.waitKey(0)
cv2.destroyAllWindows()