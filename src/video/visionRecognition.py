from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

greenLower = (40, 150, 70)
greenUpper = (70, 255, 255)

blueLower = (90,150,50)
blueUpper = (128,255,255)

yellowLower = (25,120,100)
yellowUpper = (40,255,255)

red1Lower = (0,180,70)
red1Upper = (5,255,255)

red2Lower = (160,150,70)
red2Upper = (180,255,255)

pts = deque(maxlen=args["buffer"])

# Use this to satrt stream
# gst-launch-0.10 -v v4l2src device=/dev/video-top ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! ffmpegcolorspace ! jpegenc ! multipartmux! tcpserversink port=3000

# vs = cv2.VideoCapture("tcp://192.168.252.226:3000")
# vs = cv2.VideoCapture("tcp://192.168.252.247:3000")
vs = cv2.VideoCapture("tcp://192.168.252.247:3001")
# vs = cv2.VideoCapture("tcp://192.168.253.155:3000")

while True:
    
    # grab the current frame
    frame = vs.read()
    frame = frame[1]
    # frame = frame[:, 150:]
    # frame = frame[:, :-150]
    # frame = frame[:][:240]
    # frame = cv2.Canny(frame, threshold1=123, threshold2=123)


    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of 
    # the video
    # resize the frame, blur it, and convert it to the HSV
    if frame is None:
        print ("i have no picture")
        break
    # color space
    # frame = imutils.resize(frame, width=240)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask

    gMask = cv2.inRange(hsv, greenLower, greenUpper)
    bMask = cv2.inRange(hsv, blueLower, blueUpper)
    yMask = cv2.inRange(hsv, yellowLower, yellowUpper)
    r1Mask = cv2.inRange(hsv, red1Lower, red1Upper)
    r2Mask = cv2.inRange(hsv, red2Lower, red2Upper)

    mask = gMask | bMask | yMask | r1Mask | r2Mask
    # mask = yMask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    col = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue
            
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points

            
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 2, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)
    


    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
cv2.destroyAllWindows()

