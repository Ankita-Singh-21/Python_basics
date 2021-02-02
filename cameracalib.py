#!/usr/bin/env python

import numpy as np 
import cv2
import glob
import sys
import argparse

# SET THE PARAMETERS

nRows = 5
nCols = 4
dimension = 25

working_folder = "camera_01"
imageType = 'jpg'

# termination criteria

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ........(6,5,0)
objp = np.zeros((nRows*nCols, 3), np.float32)
objp[:,:2] = np.mgrid[0:nCols, 0:nRows].T.reshape(-1,2)


# Arrays to store object points and image points from all the images
objpoints = []   # 3d point in real world space
imgpoints = []   # 2d points in image plane

if len(sys.argv) < 6:
	print("\n Not enough inputs are provided. Using the default values. \n\n")
 	print(" type -h for help")

else:
 	workingFolder = sys.argv[1]
 	imageType = sys.argv[2]
 	nRows = int(sys.argv[3])
 	nCols = int(sys.argv[4])
 	dimension = float(sys.argv[5])

if '-h' in sys.argv or '--h' in sys.argv:
 	print (" IMAGE CALIBRATION GIVEN A SET OF IMAGES")
 	print (" call: python cameracalib.py <folder> <image type> <num rows (9) > <num cols (6)> <cell dimension (25)>")
 	print (" The script will look for every image in the provided folder and will show the pattern found. ") 
 	print (" User can skip the image processing ESC or accepting the image with RETURN.")
 	print ("At the end the following files are executed:")
 	print (" - cameraDistortion.txt")
 	print ("-cameraMatrix.txt \n\n")

 	sys.exit()

# Find the image files
filename = working_folder + "/*." + imageType
images = glob.glob(filename)

print(len(images))
if len(images) < 9:
	print("Not enough images were found: at least 9 shall be provided")
	sys.exit()

else:
	nPatternFound = 0
	imgNotGood = images[1]

	for fname in images:
		if 'calibresult' in fname: continue

		# --Read the file and convert in greyscale

		img = cv2.imread(fname)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		print ("Reading image", fname)

		# Find the chess board corners
		ret, corners = cv2.findChessboardCorners(gray, (nCols,nRows), None)
		print(ret)



		# If found, add object points, image points (after refining them)

		if ret == True:
			print("yha_tak")
			print("Pattern found! Press ESC to skip or ENTER to accept")
			# --- Sometimes, Harris corners fails with crappy pictures, so
			corners2 = cv2.cornerSubPix(gray, corners,(11,11),(-1,-1), criteria)

			# Draw and display the corners
			cv2.drawChessboardCorners(img, (nCols,nRows), corners2, ret)
			cv2.imshow('img', img)

			# cv2.waitKey(0)
			k = cv2.waitKey(0) & 0xff

			# ---- ESC button 
			if k == 27:
				print("Image Skipped")
				imgNotGood = fname
				continue

			print("Image accepted")
			nPatternFound += 1
			objpoints.append(objp)
			imgpoints.append(corners2)

			# cv2.waitKey(0)
		else:
			imgNotGood = fname

cv2.destroyAllWindows()

if (nPatternFound > 1):
	print (" Found %d good images" % (nPatternFound))
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
	(objpoints, imgpoints, gray.shape[::-1],None,None)

	# Undistort an image
	img = cv2.imread(imgNotGood)
	h, w = img.shape[:2]

	print ("Image to undistort:" , imgNotGood)
	newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

	# undistort
	mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
	dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)


	# crop the image
	x,y,w,h = roi
	dst = dst[y:y+h, x:x+w]
	print("ROI: ", x,y,w,h)


	cv2.imwrite(working_folder + "/calibresult.png",dst)
	print ("Calibrated picture saved as calibresult.png")
	print ("Calibration Matrix :")
	print(mtx)
	print("Distortion :", dist)

	# ----- Save result
	filename = working_folder + "/cameraMatrix.txt"
	np.savetxt(filename, mtx, delimiter=',')
	filename = working_folder + "/cameraDistortion.txt"
	np.savetxt(filename, dist, delimiter=',')

	mean_error = 0
	for i in xrange(len(objpoints)):
		imgpoints2, _ =cv2.projectPoints(objpoints[i], ret[i], tvecs[i], mtx,dst)
		error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoiunts2)
		mean_error += mean_error

	print ("total error: ", mean_error/len(objpoints))

else:
	print(" In order to calibrate you need atleast 9 good pictures...  try again")













































































































