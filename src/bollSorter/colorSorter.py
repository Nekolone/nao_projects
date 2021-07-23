import qi, time, sys
from eventmanager import *
from colorDetector import *
from service import video, tts, memory, motion, alife, posture, atts, touch


def main():
    green = Color("green", (40, 150, 70), (70, 255, 255))
    blue = Color("blue", (100, 150, 50), (128, 255, 255))
    yellow = Color("yellow", (25, 120, 100), (40, 255, 255))
    red1 = Color("red", (0, 180, 70), (5, 255, 255))
    red2 = Color("red", (160, 150, 70), (180, 255, 255))

    global objectColorDetector
    objectColorDetector = PictureColorDetector([green, blue, yellow, red1, red2], 500, 1)

    motion.stopMove()
    alife.setState("safeguard")
    posture.goToPosture("Stand", 0.4)

    motion.setMoveArmsEnabled(True, False)  # (left,right)
    motion.moveTo(0, -0.001, 0)

    defState()

    tts.say("give me an object and I'll say what color it is and put it into the corresponding box")
    time.sleep(2)

    # print objectColorDetector.getColor()

    global eventHandler
    eventHandler = Eventloop()
    eventHandler.addEvent(
        Event(exit, [], binaryPredicate(lambda: touch.getStatus()[8][1], True, False), single_use=True, threadable=True))
    eventHandler.addEvent(Event(checkColor, [], binaryPredicate(lambda: touch.getStatus()[7][1], True, False)))
    eventHandler.start()
    eventHandler.join()
    posture.goToPosture("Stand", 0.4)

def exit():
    eventHandler.stop()
    motion.stopMove()
    posture.goToPosture("Stand", 0.4)
    sys.exit(0)


def defState():
    motion.stiffnessInterpolation("LShoulderPitch", 0.3, 0.5)
    motion.stiffnessInterpolation("LElbowRoll", 0.3, 0.5)
    motion.stiffnessInterpolation("LElbowYaw", 0.3, 0.5)
    motion.stiffnessInterpolation("LWristYaw", 0.3, 0.5)
    motion.stiffnessInterpolation("LHand", 0.3, 0.5)
    motion.setAngles("LShoulderPitch", 1, 0.1)
    motion.setAngles("LElbowRoll", -1.4, 0.1)
    motion.setAngles("LElbowYaw", -1.5, 0.1)
    motion.setAngles("LWristYaw", -1.8, 0.4)
    motion.openHand("LHand")
    motion.setAngles("HeadYaw", 0.6, 0.1)
    motion.setAngles("HeadPitch", 0, 0.1)


def checkColor():
    motion.stiffnessInterpolation("LHand", 0.3, 0.5)
    motion.closeHand("LHand")
    tts.say("hmm what is this?")
    objColor = objectColorDetector.getColor()
    if objColor == []:
        tts.say("i can't understand what color it is")
        goBack(0)
        return
    tts.say("i think this is {} object".format(objColor))
    c = findColoredBox(objColor)
    goBack(c)


def goBack(c):
    for i in range(c):
        motion.moveTo(0, 0.15, 0)
    defState()
    tts.say("give me next object")


def findColoredBox(color):
    motion.setAngles("HeadYaw", 0, 0.1)
    motion.setAngles("HeadPitch", 0.48, 0.1)
    time.sleep(2)
    for i in range(4):
        objColor = objectColorDetector.getColor()
        tts.say("i think this is {} box".format(objColor))
        if color == objColor:
            dropThisBall()
            return i
        if i != 3:
            motion.moveTo(0, -0.15, 0)
    for i in range(4):
        objColor = objectColorDetector.getColor()
        tts.say("i think this is {} box".format(objColor))
        if color == objColor:
            dropThisBall()
            return 3 - i
        if i != 3:
            motion.moveTo(0, 0.15, 0)

    tts.say("i cant sort this item")
    return 0

    # objColor = objectColorDetector.getColor()
    # tts.say("i think this is {} box".format(objColor))
    # time.sleep(0.5)
    # objColor = objectColorDetector.getColor()
    # tts.say("i think this is {} box".format(objColor))
    # motion.moveTo(0, -0.15, 0)
    # time.sleep(0.5)
    # objColor = objectColorDetector.getColor()
    # tts.say("i think this is {} box".format(objColor))
    # motion.moveTo(0, -0.15, 0)
    # time.sleep(0.5)
    # objColor = objectColorDetector.getColor()
    # tts.say("i think this is {} box".format(objColor))
    # motion.moveTo(0, -0.15, 0)


def dropThisBall():
    motion.setAngles("LShoulderPitch", 1, 0.1)
    motion.setAngles("LElbowRoll", -1.4, 0.1)
    motion.setAngles("LElbowYaw", -1, 0.1)
    motion.setAngles("LWristYaw", 1.2, 0.4)
    time.sleep(1)
    motion.openHand("LHand")
    # motion.stiffnessInterpolation("LHand",0.3,0.5)
    # motion.setAngles("LElbowYaw", -1.5, 0.1)
    # motion.setAngles("LWristYaw", -1.8, 0.4)
    # eventHandler.stop()


main()

# motion.closeHand("RHand")
# motion.stiffnessInterpolation("RHand",1,0.5)
