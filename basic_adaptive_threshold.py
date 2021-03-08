'''
Adaptive Thresholding as the name suggests , does not threshold pixels with 
global values, but with local values, according to nearby pixel. It 
is just like "andho me kana raja chuno" .


The adaptiveMethod decides how the threshold value is calculated:

cv.ADAPTIVE_THRESH_MEAN_C: 

The threshold value is the mean of the neighbourhood area minus the constant C.
cv.ADAPTIVE_THRESH_GAUSSIAN_C: 
The threshold value is a gaussian-weighted sum of the neighbourhood values minus 
the constant C.

The blockSize determines the size of the neighbourhood area and C is a constant 
that is subtracted from the mean or weighted sum of the neighbourhood pixels.

'''

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt



path = '/home/ankita/Documents/Opencv/images/sketch.jpg'

img1 = cv.imread(path)
img1 = cv.resize(img1 , (400,400))
img_grey = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img = cv.medianBlur(img_grey,5)

ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2);
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2);

titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
images = [img, th1, th2, th3]

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()