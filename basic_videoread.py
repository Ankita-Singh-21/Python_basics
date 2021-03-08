import cv2

frameWidth = 640
frameHeight = 360

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('name_of_video')

cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
	success,img=cap.read()
	cv2.imshow("Video" , img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()