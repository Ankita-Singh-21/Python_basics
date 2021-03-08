import numpy as np 
import cv2

path1 = '/home/ankita/Documents/Opencv/images/messi.jpeg'
img1 = cv2.imread(path1)

img1= cv2.resize(img1,(512,512))

print(img1.shape) # return a tuple of number of rows,columns and channel
print(img1.size) # return total number of pixel
print(img1.dtype)  # return image data type
b,g,r= cv2.split(img)
img = cv2.merge((b,g,r))

# [y1:y2 , x1:x2]
ball = img1[445:500, 305:360]
img1[450:505, 60:115]= ball 

# to add two image
#cv.add(img1,img2)

# to add according to weight
#(image1, alpha, image2, beta, gamma)
#cv.addWeighted(img1, .9 , img2, .1, 1)

cv2.imshow('image', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()



