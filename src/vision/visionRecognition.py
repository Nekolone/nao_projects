from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# import qi

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

greenLower = (40, 150, 70)
greenUpper = (70, 255, 255)

blueLower = (100,150,50)
blueUpper = (128,255,255)
# blueLower = (116,50,50)
# blueUpper = (130,255,255)

# cyanLower = (90,150,170)
# cyanUpper = (114,255,255)
# redLower = (45, 150, 70)
# redUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# # to the webcam
# if not args.get("video", False):
#     vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file

# vs = cv2.VideoCapture("tcp://192.168.252.226:3000")
# allow the camera or video file to warm up
time.sleep(2.0)

# global video

# ip = "192.168.252.226"
# # ip = "192.168.252.62"

# session = qi.Session()
# session.connect("tcp://" + ip + ":" + "9559")
# video = session.service( "ALVideoDevice" )   
# memory = session.service( "ALMemory" )

# qi.os.system("nao stop")



# videoClient = video.subscribeCamera("myCam",0,2,13,30)
# print video.getSubscribers()

vs = cv2.VideoCapture("tcp://192.168.252.226:3000")

while True:
    # naoVideo = video.getImagesRemote(videoClient)
    
    # grab the current frame
        # frame = video.getDirectRawImageRemote(videoClient)
        # video.releaseDirectRawImage(videoClient)


        # frame = np.reshape(frame[6],(-1,frame[0],3))
        # print len(frame)
        # print frame

    frame = vs.read()
    frame = frame[1]


    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of 
    # the video
    # resize the frame, blur it, and convert it to the HSV
    if frame is None:
        print ("help me")
        break
    # color space
    frame = imutils.resize(frame, width=640)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    print len(hsv)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    gMask = cv2.inRange(hsv, greenLower, greenUpper)
    bMask = cv2.inRange(hsv, blueLower, blueUpper)

    mask = gMask | bMask
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
            col = np.argmax(frame[center[1],center[0]])
            print col

            # only proceed if the radius meets a minimum size
            # if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 2, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)
    # bgrCheck = frame[center[1],center[0]]

    # col = max(bgrCheck)
    print col
    # col = np.argmax(bgrCheck)
    # bgrCheck.index(max(bgrCheck))

    if col == 0:
        print "blue"
    elif col == 1:
        print "green"
    # elif col == 2:
    #     print "red"


    # loop over the set of tracked points
    # for i in range(1, len(pts)):
    #     # if either of the tracked points are None, ignore
    #     # them
    #     if pts[i - 1] is None or pts[i] is None:
    #         continue
    #     # otherwise, compute the thickness of the line and
    #     # draw the connecting lines
    #     thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    #     cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream

# otherwise, release the camera
# vr.release()
# video.unsubscribe(videoClient)
# close all windows
cv2.destroyAllWindows()

