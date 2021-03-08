import cv2

path='/home/ankita/Documents/Opencv/images/shapes.jpeg'

img= cv2.imread(path)
img=cv2.resize(img, (800,400))

cv2.imshow("image" , img)

cv2.waitKey(0)
cv2.destroyAllWindows()