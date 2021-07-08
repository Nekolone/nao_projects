import qi, time
from eventmanager import *
from colorDetector import *
from service import video, tts, memory, motion, alife, posture, atts, touch


def main():
    green = Color("green", (40, 150, 70), (70, 255, 255))
    blue = Color("blue", (100, 150, 50), (128, 255, 255))


    global objectColorDetector
    objectColorDetector = PictureColorDetector([green, blue], 500, 1)


    motion.stopMove()
    alife.setState("safeguard")
    posture.goToPosture("Stand",0.4)

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
    tts.say("give me an object and i say what color it is")
    time.sleep(2)

    # print objectColorDetector.getColor()

    global eventHandler
    eventHandler = Eventloop()
    eventHandler.addEvent(Event( eventHandler.stop, [], binaryPredicate(lambda: touch.getStatus()[8][1], True, False), single_use= True))
    eventHandler.addEvent(Event( checkColor, [], binaryPredicate(lambda: touch.getStatus()[7][1], True, False)))
    eventHandler.start()
    eventHandler.join()
    posture.goToPosture("Stand",0.4)


def checkColor():    
    motion.stiffnessInterpolation("LHand",0.3,0.5)
    motion.closeHand("LHand")
    motion.stiffnessInterpolation("LHand",1,0.5)
    tts.say("hmm what is this?")
    objColor = objectColorDetector.getColor()
    tts.say("i think this is {} object".format(objColor))
    dropThisBall(objColor)

def dropThisBall(color):
    if color == []:
        tts.say("but i have no idea what it is")
        motion.openHand("LHand")    
        return
    if color[0] == "green":
        motion.setAngles("LElbowYaw", -1, 0.1)
        motion.setAngles("LWristYaw", 1.2, 0.4)
    if color[0] == "blue":
        motion.setAngles("LElbowYaw", -2, 0.1)
        motion.setAngles("LWristYaw", 1.7, 0.4)
    time.sleep(1)
    motion.openHand("LHand")    
    motion.stiffnessInterpolation("LHand",0.3,0.5)
    motion.setAngles("LElbowYaw", -1.5, 0.1)
    motion.setAngles("LWristYaw", -1.8, 0.4)
    tts.say("give me next object")
    # eventHandler.stop()

main()



# motion.closeHand("RHand")
# motion.stiffnessInterpolation("RHand",1,0.5)

