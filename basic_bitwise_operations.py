''' Note :- cv2.add just add two images of same size according
 to its pixel values , if it ig greater than 255, then its
  value will be 255 only
 '''

import numpy as np 
import cv2
from matplotlib import pyplot as plt

path1 = '/home/ankita/Documents/Opencv/images/messi.jpeg'
img1 = cv2.imread(path1)
img1 = cv2.cvtColor(img1 , cv2.COLOR_BGR2RGB)

img1= cv2.resize(img1,(512,512))
img1_cp= cv2.resize(img1,(512,512))

path2 = '/home/ankita/Documents/Opencv/images/opencv.png'
img2 = cv2.imread(path2)
img2 = cv2.cvtColor(img2 , cv2.COLOR_BGR2RGB)
img2 = cv2.resize(img2,(300,300))
img2_cp = cv2.resize(img2,(300,300))

# I want to put logo on top-left corner, So I create a ROI
rows,cols,channels = img2.shape
rows_cp,cols_cp,channels_cp = img2_cp.shape
roi = img1[0:rows, 0:cols]
roi_cp = img1_cp[0:rows_cp, 0:cols_cp]

# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)


# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)

# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img2,img2,mask = mask)

# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
img1[0:rows, 0:cols ] = dst

titles = ['image1','image2','roi' ,'mask','mask_inv',
'roi_and_maskinv(a)','image2andmask(b)','add_(a)_(b)','final_image']
images = [img1_cp,img2_cp,roi_cp,mask,mask_inv,img1_bg,img2_fg, dst , img1]

for i in range(len(titles)):
    plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()