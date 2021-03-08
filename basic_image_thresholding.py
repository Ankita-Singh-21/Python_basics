import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt



path = '/home/ankita/Documents/Opencv/images/stamp_college.png'
img = cv.imread(path)
img = cv.cvtColor(img,cv.COLOR_BGR2RGB)

# image below 127 is 0 or black
ret,thresh1 = cv.threshold(img,50,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in xrange(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
