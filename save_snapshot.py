

# Save a series of snapshots with the current camera as snapshot_<width>_<height>_<nnn>.jpg

import cv2
import time
import sys
import argparse
import os

def save_snaps(width , height , name = "snapshot", folder = "jipi"):

	cap = cv2.VideoCapture(0)
	print('hello')
	if width > 0 and height > 0:
		print ("Setting the custom Width and Height")
		cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



	try:

		if not os.path.exists(folder):
			print('yha tak1')


			# create the folder
			os.makedirs(folder)
			folder = os.path.dirname(folder)
			print('hello3')
			try:
				os.stat(folder)
			except:
				os.mkdir(folder)

	except:
		print('hello8')
		pass


	nSnap = 200

	w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
	h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

	fileName = "%s/%s_%d_%d" %(folder, name, w,h)
	while True:
		ret, frame = cap.read()
		cv2.imshow("Video", frame)

		print ("Saving image ", nSnap)
		cv2.imwrite("%s%d.jpg"%(fileName, nSnap), frame)
		nSnap +=1
		

		'''key = cv2.waitKey(1) & 0xFF
		if key == ord('a'):
			break

		
		if key == ord('i'):
			print ("Saving image ", nSnap)
			cv2.imwrite("%s%d.jpg"%(fileName, nSnap), frame)
			nSnap +=1

		#print('t')'''

	cap.release()
	cv2.destroyAllWindows()



def main():
	print('hello1')

	SAVE_FOLDER = "jipi"
	FILE_NAME = "snapshot"
	FRAME_WIDTH = 0
	FRAME_HEIGHT = 0

	parser = argparse.ArgumentParser(description = "Saves snapshot from the camera. \n q to quit \n spacebar to save the snapshot")
	parser.add_argument("--folder", default = SAVE_FOLDER, help = "Path to the save folder(default:current)")
	parser.add_argument("--name", default = FILE_NAME, help = "Picture file name (default: snapshot)")
	parser.add_argument("--dwidth", default = FRAME_WIDTH, type = int, help = "<width> px (default the camera output)")
	parser.add_argument("--dheight", default = FRAME_HEIGHT, type = int, help = "<height> px (default the camera output)")
	

	args = parser.parse_args()

	SAVE_FOLDER = args.folder
	FILE_NAME = args.name
	FRAME_WIDTH = args.dwidth
	FRAME_HEIGHT = args.dheight

	save_snaps (width = args.dwidth, height = args.dheight, name = args.name,folder = args.folder)

	print "Files saved"

if __name__ == "__main__":
	
	main()
	








































