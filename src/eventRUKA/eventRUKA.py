# -*- encoding: UTF-8 -*-

import time
import threading
import random

# Если нет доступа к PATH
# import sys, os
# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
# sys.path.append(path + '\custom_lib')
# 

from eventmanager import Eventloop, EventGroup, Event, binaryPredicate, changedValuePredicate

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule



def eventRuka(robot_IP, robot_PORT=9559):

    global tts, memory, motion, alife, touch, posture
    
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    memory = ALProxy("ALMemory",robot_IP,robot_PORT)
    motion = ALProxy("ALMotion", robot_IP, robot_PORT)    
    posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
    alife = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
    touch = ALProxy("ALTouch", robot_IP, robot_PORT)



    global phrases      #   фразы при движении
    phrases = {
        "general": ["what a great day", "I'm not just some kind of robot as you might think, I'm something more"],
        "general_repeat": ["and you are good at copying me human", "good"],
        "general_move": ["ok let's go here", "lead me"],
        "general_move_repeat": ["I'm tired, let's stand", "you walk well, for human of course. ha ha ha", "Where are we going? Don't say! Let it be a secret",
            "Color seem brihter when you are around", "not tired yet, human?", "don't hurt my hand", "you are doing good", "Not so fast", "it's nice to walking with you",
            "It my best walking! On a scale from 1 to 10, it's an 11", "Any walk drives away gloomy thoughts", "when you are not in the mood, take a walk with people close to you in places dear to you",
            "Today i want to walk to my full height: let's go to the park and sit on bench", "Let's go left or right"],
        "forward": ["ok let's go forward", "to infinity and beyond", "Not so fast"],
        "forward_repeat": ["wait i'm tired"],
        "backward": ["watch the rear", "ok let's go backward", "ouch ouch ouch ... be gentle"],
        "backward_repeat": ["wait i'm tired"],
        "turn_left": ["ok let's go left", "going west"],
        "turn_left_repeat": ["I got dizzy"],
        "turn_right": ["ok let's go right", "going east"],
        "turn_right_repeat": ["I got dizzy"],
        "forward_left": ["Port!"],
        "forward_left_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?", "I'm having fun with you, but we go in circles"],
        "forward_right": ["Starboard!"],
        "forward_right_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?", "I'm having fun with you, but we go in circles"],
        "backward_left": ["ok let's go left"],
        "backward_left_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?", "I'm having fun with you, but we go in circles"],
        "backward_right": ["ok let's go right"],
        "backward_right_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?", "I'm having fun with you, but we go in circles"],
        "stop": ["and we stand again"],
        "stop_repeat": ["why are we standing?", "can we go already?", "tired of just standing still", "come on, take my hand and go for a walk", "sounds of falling asleep NAO"]
    }

    alife.setState("disabled")
    
    motion.stopMove()
    motion.wakeUp()
    motion.setMoveArmsEnabled(True, False) #(left,right)

    tts.post.say("Take my hand and let's go for a walk")
    motion.post.setAngles("RShoulderPitch", -1.5, 0.4)    
    motion.post.setAngles("RShoulderRoll", 0, 0.4)
    motion.openHand("RHand")

    global loop
    loop = True




    global eventHandler, phraseGen

    phraseGen = PhraseGenerator()

    #   Создание экземпляра класса Eventloop
    eventHandler = Eventloop()
    #   eventHandler.addGroup(EventGroup)
    #   eventHandler.addEvent(Event(lambda: Предикат(проверка), Функция, Аргументы, single_use=False, threadable=True, cooldown=0))

    #   Создание групп ивентов
    motionGroup = EventGroup()
    ttsGroup = EventGroup(cooldown = 11)
    #   generalGroup.addEvent(Event(lambda: Предикат(проверка), Функция, Аргументы, single_use=False, threadable=True, cooldown=0))


    #   Создание и добавление ивентов на обработку (по стандарту внутри уже создана группа для ивентов, не требующих определенную группу) 
    eventHandler.addEvent(Event( naoExit, [], binaryPredicate(lambda: touch.getStatus()[8][1], True, False), single_use=True))

    eventHandler.addEvent(Event( touchMyHand, [], binaryPredicate(lambda: touch.getStatus()[18][1], True, False), single_use=True, threadable=True))

    #   Создание и обьединение ивентов в группы
    motionGroup.addEvent(Event( motion.moveTo, [10,0,0], getForward , threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["forward"], getForward , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveTo, [-10,0,0], getBackward, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["backward"], getBackward , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveTo, [0,0,0.78], getLeft, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["turn_left"], getLeft , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveTo, [0,0,-0.78], getRight, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["turn_right"], getRight , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveToward, [1,0,0.5,[["Frequency", 0.1]]], getForwardLeft, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["forward_left"], getForwardLeft , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveToward, [1,0,-0.5,[["Frequency", 0.1]]], getForwardRight, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["forward_right"], getForwardRight , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveToward, [-1,0,-0.5,[["Frequency", 0.1]]], getBackwardLeft, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["backward_left"], getBackwardLeft , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.moveToward, [-1,0,0.5,[["Frequency", 0.1]]], getBackwardright, threadable=True))
    ttsGroup.addEvent(Event( walkPhrases, ["backward_right"], getBackwardright , threadable=True, cooldown=20))

    motionGroup.addEvent(Event( motion.stopMove, [], getStopMove))
    ttsGroup.addEvent(Event( walkPhrases, ["stop"], getStopMove , threadable=True, cooldown=30))
    
    #   Добавление групп в обработчик ивентов
    eventHandler.addEventGroup(motionGroup)
    eventHandler.addEventGroup(ttsGroup)

    #   Запуск обработчика ивентов
    eventHandler.start()

    #   Ожидание обработчика ивентов
    eventHandler.join()
    tts.say("It was great! Have a nice day!")
    alife.setState("interactive")


def walkPhrases(state):
    tts.say(phraseGen.getPhrase(state))


def touchMyHand():    
    motion.post.stiffnessInterpolation("RShoulderPitch",0.0,1.0)
    motion.post.stiffnessInterpolation("RShoulderRoll",0.0,1.0)
    motion.post.stiffnessInterpolation("RWristYaw",0.0,1.0)
    motion.closeHand("RHand")
    tts.say("Take my hand! Let's warm up")


def naoExit():
    global loop
    eventHandler.stop()
    loop=False
    motion.stopMove()
    posture.goToPosture("Stand",0.4)


def getRShoulderPitch():
    return motion.getAngles("RShoulderPitch",False)[0]

def getRShoulderRoll():
    return motion.getAngles("RShoulderRoll",False)[0]

def getForward():
    return -0.85 < getRShoulderPitch() and (-0.2 <= getRShoulderRoll() <= 0.1) and not getRShoulderPitch()>0.2 and loop

def getForwardLeft():
    return -0.85 < getRShoulderPitch() and 0.1 < getRShoulderRoll()  and not getRShoulderPitch()>0.2 and loop

def getForwardRight():
    return -0.85 < getRShoulderPitch() and getRShoulderRoll() < -0.2  and not getRShoulderPitch()>0.2 and loop

def getBackward():
    return getRShoulderPitch() < -1.75 and (-0.2 <= getRShoulderRoll() <= 0.1) and not getRShoulderPitch()>0.2 and loop

def getBackwardLeft():
    return getRShoulderPitch() < -1.75 and 0.1 < getRShoulderRoll()  and not getRShoulderPitch()>0.2 and loop

def getBackwardright():
    return getRShoulderPitch() < -1.75 and getRShoulderRoll() < -0.2  and not getRShoulderPitch()>0.2 and loop

def getLeft():
    return (-1.75 <= getRShoulderPitch() <= -0.85) and 0.1 < getRShoulderRoll() and not getRShoulderPitch()>0.2 and loop

def getRight():
    return (-1.75 <= getRShoulderPitch() <= -0.85) and getRShoulderRoll() < -0.2 and not getRShoulderPitch()>0.2 and loop

def getStopMove():
    return not(getForward() or getForwardLeft() or getForwardRight() or getBackward() or getBackwardLeft() or getBackwardright() or getLeft() or getRight())

class PhraseGenerator:

    def __init__(self):
        self.oldarg = None
        self.generator = self._getGenerator()

    def _getGenerator(self):
        yield random.choice(phrases["general"] + phrases[self.oldarg] + [i for i in phrases["general_move"] if self.oldarg != "stop"])
        while True:
            yield random.choice(phrases["general_repeat"] + phrases[self.oldarg+"_repeat"] + [i for i in phrases["general_move_repeat"] if self.oldarg != "stop"])
    
    def getPhrase(self, arg):
        if arg != self.oldarg:
            self.generator = self._getGenerator()
        self.oldarg = arg
        return next(self.generator)


# eventRuka("192.168.252.226", 9559)
# eventRuka("192.168.252.62", 9559)
eventRuka("192.168.253.155", 9559)
# eventRuka("192.168.253.80", 9559)
# eventRuka("NaoThree.local", 9559)
