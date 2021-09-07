import cv2
import imutils
import numpy as np

from _eventmanager import *
from service import video, tts, motion, alife, posture, touch


class Color:
    def __init__(self, name, lower_bound, upper_bound):
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


class PictureColorDetector:
    def __init__(self, colors, size, cam_num=0):
        self.colors = colors
        self.size = size
        self.video_client = video.subscribeCamera("myCam", cam_num, 2, 13, 10)

    def get_color(self):
        img = video.getImageRemote(self.video_client)
        video.releaseImage(self.video_client)

        frame = np.reshape(img[6], (-1, img[0], 3))
        frame = frame[:, 150:]
        frame = frame[:, :-150]
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = np.zeros((img[1], img[0] - 300), np.uint8)
        for color in self.colors:
            mask = mask | cv2.inRange(hsv, color.lower_bound, color.upper_bound)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        col = None
        detected_colors = []

        if len(cnts) == 0:
            return detected_colors
        c = max(cnts, key=cv2.contourArea)
        if cv2.contourArea(c) < self.size:
            return detected_colors
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        detected_colors.append(self._pixel_color(hsv[center[1], center[0]]))
        return detected_colors

    def _pixel_color(self, pixel):
        for color in self.colors:
            if pixel[0] in range(color.lower_bound[0], color.upper_bound[0] + 1):
                return color.name
        raise Exception("Impossible Error, Pixel not identified")

    def __del__(self):
        video.unsubscribe(self.video_client)


def start_sorting():
    green = Color("green", (40, 150, 70), (70, 255, 255))
    blue = Color("blue", (100, 150, 50), (128, 255, 255))
    yellow = Color("yellow", (25, 120, 100), (40, 255, 255))
    red1 = Color("red", (0, 180, 70), (5, 255, 255))
    red2 = Color("red", (160, 150, 70), (180, 255, 255))

    global object_color_detector
    object_color_detector = PictureColorDetector([green, blue, yellow, red1, red2], 500, 1)

    motion.stopMove()
    alife.setState("safeguard")
    posture.goToPosture("Stand", 0.4)

    motion.setMoveArmsEnabled(True, False)  # (left,right)
    motion.moveTo(0, -0.001, 0)

    def_state()

    tts.say("give me an object and I'll say what color it is and put it into the box")
    time.sleep(2)

    global event_handler
    event_handler = Eventloop()
    event_handler.add_event(
        Event(exit, [], binary_predicate(lambda: touch.getStatus()[8][1], True, False), single_use=True,
              threadable=True))
    event_handler.add_event(Event(check_color, [], binary_predicate(lambda: touch.getStatus()[7][1], True, False)))
    event_handler.start()
    event_handler.join()
    posture.goToPosture("Stand", 0.4)


def exit():
    event_handler.stop()
    motion.stopMove()
    posture.goToPosture("Stand", 0.4)
    # sys.exit(0)


def def_state():
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


def check_color():
    motion.stiffnessInterpolation("LHand", 0.3, 0.5)
    motion.closeHand("LHand")
    tts.say("hmm what is this?")
    obj_color = object_color_detector.get_color()
    if obj_color == []:
        tts.say("i can't understand what color it is")
        go_back(0)
        return
    tts.say("i think this is {} object".format(obj_color))
    c = find_colored_box(obj_color)
    go_back(c)


def go_back(c):
    for i in range(c):
        motion.moveTo(0, 0.15, 0)
    def_state()
    tts.say("give me next object")


def find_colored_box(color):
    motion.setAngles("HeadYaw", 0, 0.1)
    motion.setAngles("HeadPitch", 0.48, 0.1)
    time.sleep(2)
    for i in range(4):
        obj_color = object_color_detector.get_color()
        tts.say("i think this is {} box".format(obj_color))
        if color == obj_color:
            drop_this_ball()
            return i
        if i != 3:
            motion.moveTo(0, -0.15, 0)
    for i in range(4):
        obj_color = object_color_detector.get_color()
        tts.say("i think this is {} box".format(obj_color))
        if color == obj_color:
            drop_this_ball()
            return 3 - i
        if i != 3:
            motion.moveTo(0, 0.15, 0)

    tts.say("i cant sort this item")
    return 0


def drop_this_ball():
    motion.setAngles("LShoulderPitch", 1, 0.1)
    motion.setAngles("LElbowRoll", -1.4, 0.1)
    motion.setAngles("LElbowYaw", -1, 0.1)
    motion.setAngles("LWristYaw", 1.2, 0.4)
    time.sleep(1)
    motion.openHand("LHand")

if __name__ == "__main__":
    start_sorting()
