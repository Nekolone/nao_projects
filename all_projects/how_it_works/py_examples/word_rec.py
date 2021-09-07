# -*- encoding: UTF-8 -*-

import os
import sys

from naoqi import ALProxy

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
sys.path.append(path + '\custom_lib')
from eventmanager import *

def startTracking(robot_IP, robot_PORT=9559):
    global memory, motion, touch, asr, posture, alife, tts

    memory = ALProxy("ALMemory",robot_IP,robot_PORT)
    motion = ALProxy("ALMotion", robot_IP, robot_PORT)    
    touch = ALProxy("ALTouch", robot_IP, robot_PORT)
    asr = ALProxy("ALSpeechRecognition", robot_IP, robot_PORT)
    posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
    alife = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)

    alife.setState("disabled")
    asr.subscribe("WordRecognized")    
    motion.stopMove()

    asr.pause(True)
    asr.setLanguage("English")
    vocabulary = ["yes", "no"]
    asr.setVocabulary(vocabulary, False)
    asr.pause(False)

    global em
    em = Eventloop()
    em.addEvent(Event( starterExit, [], getStoptStarter, single_use=True, threadable=True))
    em.addEvent(Event(sayThis, [lambda: memory.getData("WordRecognized")[0]], changedValuePredicate(lambda: memory.getData("WordRecognized")[1]), threadable=True))
    em.start()
    em.join()

    asr.unsubscribe("WordRecognized")

def getStoptStarter():
    return touch.getStatus()[8][1]

def sayThis(text):
    tts.say(text())

def starterExit():
    global loop
    em.stop()
    loop=False
    motion.stopMove()
    posture.goToPosture("Stand",0.4)

# startTracking("192.168.252.226", 9559)
startTracking("192.168.252.62", 9559)

