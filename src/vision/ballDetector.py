# -*- encoding: UTF-8 -*-


import time
import qi
import vision_definitions

import PIL
from PIL import Image

import cv2
import numpy as np

from naoqi import ALModule, ALBroker



class Color:
    def __init__(self, name, rgb, callback):
        self.name = name
        self.rgb = rgb
        self.callback = callback

def pprint(a):
    print a

def main():
    red = Color("red", [160, 0, 0, 50], lambda x: pprint("onRed"))
    green = Color("green", [0, 150, 0, 50], lambda x: pprint("onGreen"))
    blue = Color("blue", [0, 0, 150, 50], lambda x: pprint("onBlue"))
    # yellow = Color("yellow", [150, 150, 0, 50], lambda x: pprint("onYellow"))
    # cyan = Color("cyan", [0, 150, 150, 25], lambda x: pprint("onCyan"))
    # purple = Color("purple", [150, 0, 150, 50], lambda x: pprint("onPurple"))

    global bub
    bub = ColorDetector([red, green, blue])

    bub.run()


class ColorDetector:
    """
    color detection class
    """
    def __init__(self, colors, diameter = 0.6):
        self.colors = colors
        self.loop = True      
        self.blob = session.service("ALColorBlobDetection")
        self.blob.setObjectProperties(50, diameter, "Circle")
        self.subscriber = memory.subscriber("ALTracker/ColorBlobDetected")
        # self.subscriber.signal.connect(self.onBlobDetection)
    
    def run(self):
        
        while self.loop:
            for color in self.colors:
                self.blob.setColor(*color.rgb)
                dis = self.subscriber.signal.connect(color.callback)
                print "checking " + color.name + "_---------------------"
                time.sleep(0.2)
                self.subscriber.signal.disconnect(dis)

    def __del__(self):
        memory.unsubscribe("ALTracker/ColorBlobDetected")

    # def onBlobDetection(self, a):
    #     """
    #     color detection callback
    #     """
    #     print "AHH, i see them " + self.color
    #     # print a


global video, memory, session

ip = "192.168.252.226"
# ip = "192.168.252.62"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")
# video = session.service( "ALVideoDevice" )   
memory = session.service( "ALMemory" )


main()