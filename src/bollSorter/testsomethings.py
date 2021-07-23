import time

from eventmanager import *
from colorDetector import *
from service import video, tts, memory, motion, alife, posture, atts, touch

import sys

motion.stopMove()
alife.setState("safeguard")
posture.goToPosture("Stand",0.4)
motion.setMoveArmsEnabled(True, False) #(left,right)
motion.moveTo(0,-0.001,0)
# posture.goToPosture("Crouch",0.4)


green = Color("green", (40, 150, 70), (70, 255, 255))
blue = Color("blue", (100, 150, 50), (128, 255, 255))


global objectColorDetector
objectColorDetector = PictureColorDetector([green, blue], 500, 1)

motion.stiffnessInterpolation("LShoulderPitch",0.3,0.5)
motion.stiffnessInterpolation("LElbowRoll",0.3,0.5)
motion.stiffnessInterpolation("LElbowYaw",0.3,0.5)
motion.stiffnessInterpolation("LWristYaw",0.3,0.5)
motion.stiffnessInterpolation("LHand",0.3,0.5)
motion.setAngles("LShoulderPitch", 1, 0.1)
motion.setAngles("LElbowRoll", -1.4, 0.1)
motion.setAngles("LElbowYaw", -1.5, 0.1)
motion.setAngles("LWristYaw", -1.8, 0.4)
motion.openHand("LHand")
motion.setAngles("HeadYaw", 0.6, 0.1)

time.sleep(10)
motion.setAngles("HeadYaw", 0   , 0.1)
motion.setAngles("HeadPitch", 0.48, 0.1)
# sys.exit(0)
objColor = objectColorDetector.getColor()
tts.say("i think this is {} object".format(objColor))

time.sleep(3)
print "test - 1"
motion.moveTo(0,-0.15,0)
objColor = objectColorDetector.getColor()
tts.say("i think this is {} object".format(objColor))


time.sleep(3)
print "test - 2"
motion.moveTo(0,-0.15,0)
objColor = objectColorDetector.getColor()
tts.say("i think this is {} object".format(objColor))


time.sleep(3)
print "test - 3"
motion.moveTo(0,-0.15,0)
objColor = objectColorDetector.getColor()
tts.say("i think this is {} object".format(objColor))


posture.goToPosture("Stand",0.4)

