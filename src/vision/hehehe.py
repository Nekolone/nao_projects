# -*- encoding: UTF-8 -*-


import time
import qi
import vision_definitions

import PIL
from PIL import Image

import cv2
import numpy as np

from naoqi import ALModule, ALBroker






def main():
    img = cv2.imread("C:\\Users\\tsi_nao\\Desktop\\nao_projects\\camImage.jpg", cv2.IMREAD_REDUCED_COLOR_4)

    cv2.imshow("Input Image", img)
    cv2.waitKey(0)
    
    bimg = cv2.GaussianBlur(img, (11, 11), 0)

    cv2.imshow("Input Image", bimg)
    cv2.waitKey(0)

    rgb = cv2.cvtColor(bimg, cv2.COLOR_BGR2RGB)

    mask = cv2.inRange(rgb, (100, 100, 0), (255,255,50))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    cv2.imshow("Input Image", cnts)
    cv2.waitKey(0)




main()
# import time
# import qi
# import vision_definitions

# import PIL
# from PIL import Image

# import cv2
# import numpy as np


# class (ALModule)


# def main():
#     global tts, memory, video
    
#     tts = session.service( "ALTextToSpeech" )
#     video = session.service( "ALVideoDevice" ) 
#     # vr = session.service("ALVisionRecognition")   
#     memory = session.service( "ALMemory" )
#     cbd = session.service("ALColorBlobDetection")
#     # tracker = session.service( "ALTracker" )
#     # motion = session.service("ALMotion")
#     # posture = session.service("ALRobotPosture")
#     # wr = session.service("ALWorldRepresentation")

#     # resolution = vision_definitions.kQQVGA
#     # colorSpace = vision_definitions.kYUVColorSpace

#     # resolution = 2
#     # colorSpace = 11
#     # fps = 20

#     videoClient = video.subscribeCamera("myCam",0,3,11,5)
#     naoImage = video.getImageRemote(videoClient)
#     # video.unsubscribe(videoClient)

#     imageWidth = naoImage[0]
#     imageHeight = naoImage[1]
#     array = naoImage[6]
#     image_string = str(bytearray(array))
#     im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

#     cbd.setColor(255-15,0,0, 255)
#     cbd.setObjectProperties(10, 0.1, "Unknown")
#     memory.subscribeToEvent("ALTracker/ColorBlobDetected", "BallDetector", "onBlobDetection")
#     print("BallDetector initialized!")
#     # threading.Lock()

#     got_color = False

#     try:
#         while True:
#             print "helpme"
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print "Interrupted by user, stopping"
#         # vr.unsubscribe("ALTracker/ColorBlobDetected")
#         #stop
#         video.unsubscribe(videoClient)
#         sys.exit(0)


# def onBlobDetection(eventName, value, subscriberIdentifier):
#     print "HELPMEEEE"
#     positionInFrameRobot = value[1]
#     print("Ball detected.")
#     timestampUS = value[2][1]
#     tts.say("o ball")

#     # im.save("camImage.png", "PNG")

#     # img = cv2.imread("C:\\Users\\tsi_nao\\Desktop\\nao_projects\\camImage.png", cv2.IMREAD_GRAYSCALE)

#     # cv2.imshow("Input Image", img)
#     # cv2.waitKey(0)


#     # params = cv2.SimpleBlobDetector_Params()

#     # params.filterByColor = 1
#     # params.blobColor = 255
#     # params.filterByArea = 1
#     # params.minArea = 0
#     # params.maxArea = 10000
#     # params.filterByCircularity=0
#     # params.filterByConvexity  =0
#     # params.filterByInertia  =0





#     # detector = cv2.SimpleBlobDetector_create()
#     # keyppoint_info = detector.detect(img)
#     # blank_img = np.zeros((1,1))
#     # blobs = cv2.drawKeypoints(img, keyppoint_info, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#     # cv2.imshow("displaying blobs", blobs)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()

    


# # ip = "192.168.253.155"
# # ip = "192.168.252.62"
# ip = "192.168.252.226"
# # ip = "192.168.252.62"

# session = qi.Session()
# session.connect("tcp://" + ip + ":" + "9559")


# main()




    # print 'getting images in remote'
    # for i in range(0, 20):
    #     print "getting image " + str(i)
    #     video.getImageRemote(nameId)
    #     time.sleep(0.05)

    # video.unsubscribe(nameId)



#     cbd.setColor(255-15,0,0, 255)
#     cbd.setObjectProperties(10, 0.1, "Unknown")
#     memory.subscribeToEvent("ALTracker/ColorBlobDetected", "colorDetector", "onBlobDetection")
#     print("BallDetector initialized!")
#     threading.Lock()

#     got_color = False

#     try:
#         while True:
#             print "helpme"
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print "Interrupted by user, stopping"
#         # vr.unsubscribe("ALTracker/ColorBlobDetected")
#         #stop
#         sys.exit(0)


# def onBlobDetection(eventName, value, subscriberIdentifier):
#     positionInFrameRobot = value[1]
#     print("Ball detected.")
#     timestampUS = value[2][1]
#     tts.say("o ball")


# def on_blob_detected(value, smt, smt2):
#     print value
#     print smt
#     print smt2
#     global got_color
#     if value == []:  # empty value when the recognized object disappears
#         got_color = False
#     elif not got_color:  # only speak the first time a recognized object appears
#         got_color = True
#         print "I saw a this! "
#         tts.say("I saw a this! ")
#         # First Field = TimeStamp.
#         timeStamp = value[0]
#         print "TimeStamp is: " + str(timeStamp)
#         object_data = value[1]
#         print "Object data: " + str(object_data)









    
    # # print mem.getDataListName()
    # # print mem
    # a=[]

    # for i in range(30):
    #     time.sleep(1)
    #     a.append ({
    #         "autonomous/state": mem.getData("autonomous/state"),
    #         "fall-recovery/solitary": mem.getData("fall-recovery/solitary"),
    #         "fall-recovery/failed": mem.getData("fall-recovery/failed"),
    #         "AppsAnalytics/stats": mem.getData("AppsAnalytics/stats"),
    #         "fall-recovery/previousPostureFamily": mem.getData("fall-recovery/previousPostureFamily"),
    #         "fall-recovery/recover": mem.getData("fall-recovery/recover"),
    #         # "fall-recovery", mem.getData("fall-recovery"),
    #         "Launchpad/Posture": mem.getData("Launchpad/Posture"),
    #         "Launchpad/WavingDetection": mem.getData("Launchpad/WavingDetection"),
    #         "Launchpad/PostureFamily": mem.getData("Launchpad/PostureFamily"),
    #         "Launchpad/RobotFellRecently": mem.getData("Launchpad/RobotFellRecently"),
    #         "ALTracker/BaseTracking": mem.getData("ALTracker/BaseTracking"),
    #         "BarcodeReader/BarcodeDetected": mem.getData("BarcodeReader/BarcodeDetected"),
    #         "ALTracker/ActiveTargetChanged": mem.getData("ALTracker/ActiveTargetChanged"),
    #         "ALTracker/TargetDetected": mem.getData("ALTracker/TargetDetected"),
    #         "ALAnimatedSpeech/EndOfAnimatedSpeech": mem.getData("ALAnimatedSpeech/EndOfAnimatedSpeech"),
    #         "ALTracker/ObjectMoveTo": mem.getData("ALTracker/ObjectMoveTo"),
    #         "ALTracker/TargetLost": mem.getData("ALTracker/TargetLost"),
    #         "ALTracker/ObjectLookAt": mem.getData("ALTracker/ObjectLookAt"),
    #         "RecoLatency": mem.getData("RecoLatency"),
    #         "SpeechDetected": mem.getData("SpeechDetected"),
    #         "ALTextToSpeech/TextInterrupted": mem.getData("ALTextToSpeech/TextInterrupted"),
    #         "ALTextToSpeech/CurrentSentence": mem.getData("ALTextToSpeech/CurrentSentence"),
    #         "ALTextToSpeech/CurrentWor": mem.getData("ALTextToSpeech/CurrentWord"),
    #         "ALTextToSpeech/PositionOfCurrentWord": mem.getData("ALTextToSpeech/PositionOfCurrentWord"),
    #         "ALTextToSpeech/CurrentBookMark": mem.getData("ALTextToSpeech/CurrentBookMark"),
    #         "ALTextToSpeech/TextDone": mem.getData("ALTextToSpeech/TextDone"),
    #         "_ALBrightnessStatistics/Std": mem.getData("_ALBrightnessStatistics/Std"),
    #         "VisualSpaceHistory/VisualGrid/Data": mem.getData("VisualSpaceHistory/VisualGrid/Data"),
    #         "PictureDetected": mem.getData("PictureDetected"),
    #         "FaceDetected": mem.getData("FaceDetected"),
    #         "FaceDetection/FaceDetected": mem.getData("FaceDetection/FaceDetected"),
    #         "redBallDetected": mem.getData("redBallDetected"),
    #         "ALTracker/ColorBlobDetected": mem.getData("ALTracker/ColorBlobDetected"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeZ/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeY/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeXZeroOffset/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeXZeroOffset/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeX/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyrZ/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyrZ/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyrY/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyrX/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeYZeroOffset/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeYZeroOffset/Sensor/Value"),
    #         "Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value": mem.getData("Device/SubDeviceList/InertialSensor/GyroscopeZZeroOffset/Sensor/Value"),
    #         "ALMotion/RobotIsStand": mem.getData("ALMotion/RobotIsStand"),
    #         "ALMotion/Safety/RobotOnASlope": mem.getData("ALMotion/Safety/RobotOnASlope"),
    #         "ALMotion/RobotPushed": mem.getData("ALMotion/RobotPushed")
    #     })

    # for ky in a[0].keys():
    #     print ky + "-> \\/"
    #     for pr in a:
    #         print pr[ky]




