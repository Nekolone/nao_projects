# -*- encoding: UTF-8 -*- 

import time
import threading

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from threading import Thread

rainbow=[0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff,
         0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff] 

white = 0x00ffffff

speed = 0.2
rotate_speed = 0.01


def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)

    leds.reset("AllLeds") 

    global rArmIsActive, lArmIsActive
    rArmIsActive, lArmIsActive = True,True


    while True:

        threadRArm = Thread(target=touchRArm, args=(leds,touch,"RArm","RightFaceLed{}"))
        threadLArm = Thread(target=touchLArm, args=(leds,touch,"LArm","LeftFaceLed{}"))
        #   создание двух потоков
        if lArmIsActive:
            threadLArm.start()
                                #   В случае если не запущен поток, запускает его
        if rArmIsActive:
            threadRArm.start()
        
        time.sleep(0.1) 


def touchRArm(leds,touch,sensor,led):
    global rArmIsActive
    rArmIsActive = False
    while 1:

        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    for i in range(8):
                            leds.fadeRGB(led.format(i+1), rainbow[i], speed)
                else:
                    rArmIsActive = True
                    return
                
                time.sleep(1)
                while 1:
                    for i in range(8):
                        for j in range(8):
                            leds.fadeRGB(led.format(8-j), rainbow[i+j], rotate_speed)

                            status = touch.getStatus()
                            for e in status:
                                if e[0] == sensor and e[1]==True:
                                    for i in range(8):
                                        leds.fadeRGB(led.format(i+1), white,speed)
                                    rArmIsActive = True
                                    return

def touchLArm(leds,touch,sensor,led):
    global lArmIsActive
    lArmIsActive = False
    while 1:

        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    for i in range(8):
                            leds.fadeRGB(led.format(8-i), rainbow[i], speed)
                else:
                    lArmIsActive = True
                    return
                
                time.sleep(1)
                while 1:
                    for i in range(8):
                        for j in range(8):
                            leds.fadeRGB(led.format(j+1), rainbow[i+j], rotate_speed)

                            status = touch.getStatus()
                            for e in status:
                                if e[0] == sensor and e[1]==True:
                                    for i in range(8):
                                        leds.fadeRGB(led.format(8-i), white,speed)
                                    lArmIsActive = True
                                    return


main("192.168.252.226", 9559)