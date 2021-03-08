'''
There are two types of filter. High pass filter and low pass filter. Low pass filter are used to remove noises by making all pixel values almost uniform. High pass filter are use for sharpening the images. In an image, 
there are lots of pixel. Processing each and every pixel is highly computational. 
So we lessen the number of pixel by convolving an image through a desired kernel and getting an average image with less number of pixel.  Applying filter to image means convolving a
 known matrix across whole image and finding mean value 
using various types of method.

Main function types :
cv.filter2D :- simply convolving a known kernel , most simple type of blurring
cv.GaussianBlur :- convolving a gaussian kernel, kernel is most weighted at middle
cv.medianBlur :- convolving a known kernel, finding mean value , useful in salt and pepper noise
cv.bilateralFilter :- A special type of filter to preserve edges, 

is highly effective in noise removal while keeping edges sharp. But the operation is slower compared to other filters.
 We already saw that a Gaussian filter takes the neighbourhood around the pixel and finds its Gaussian weighted average. 
 This Gaussian filter is a function of space alone, that is, nearby pixels are considered while filtering.
  It doesn't consider whether pixels have almost the same intensity. It doesn't consider whether a pixel is an edge pixel or not.
   So it blurs the edges also, which we don't want to do.

Bilateral filtering also takes a Gaussian filter in space, but one more Gaussian filter which is a function of pixel difference.
 The Gaussian function of space makes sure that only nearby pixels are considered for blurring, while the Gaussian function of 
 intensity difference makes sure that only those pixels with similar intensities to the central pixel are considered for blurring. 
 So it preserves the edges since pixels at edges will have large intensity variation.


'''

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

path1 = '/home/ankita/Documents/Opencv/images/vegetables.jpeg'
img = cv.imread(path1)
img = cv.resize(img , (800,800))
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(imgGray,-1,kernel)

blur = cv.GaussianBlur(imgGray,(5,5),0)

path2 = '/home/ankita/Documents/Opencv/images/salt_n_pepper.jpeg'
img2 = cv.imread(path2)
img2 = cv.resize(img2 , (800,800))
img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
#kernel2 = np.ones((3,3),np.float32)/25
median = cv.medianBlur(img2, 7)


b_fil = cv.bilateralFilter(img,9,75,75)


titles = ['Original Image','Gray','Averaging','GAUSSIAN_BLUR','Original','median_blur',
'Original','bilateralFilter']
images = [img,imgGray, dst, blur,img2,median, img, b_fil]


fig = plt.figure(figsize=(10, 9))
for i in xrange(len(titles)):
    fig.add_subplot(4,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()

cv.waitKey(0)
cv.destroyAllWindows()