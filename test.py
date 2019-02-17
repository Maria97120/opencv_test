# encoding=utf-8
import argparse
import datetime
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())


if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

firstFrame = None

while True:
	(grabbed, frame) = camera.read()
	text = "Unoccupied"

	if not grabbed:
		break


	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if firstFrame is None:
		firstFrame = gray
		continue

	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	thresh = cv2.dilate(thresh, None, iterations=2)
	thresh, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # cv2.findContours()函数返回三个值，第一个返回了你所处理的图像，第二个是轮廓本身，第三个是每条轮廓对应的属性


	for c in contours:
		# if the contour is too small, ignore it
		print cv2.contourArea(c)
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1)

	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()