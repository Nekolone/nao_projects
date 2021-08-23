# -*- encoding: UTF-8 -*- 

import time
import argparse
import threading
import sys

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from threading import Thread


# class SchoolTasks:

#     __init__(self, arg):
#         self.field = arg
#         self.field2 = [1,2]

#     def foo(self):
#         self.field2 * 2321312

    

    


# o = SchoolTasks(123)
# o.field3 = "dasd"

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
    rArmIsActive, lArmIsActive = 0,0

    while True:
        threadRArm = Thread(target=touchRArm, args=(leds,touch,"RArm","RightFaceLed{}"))
        threadLArm = Thread(target=touchLArm, args=(leds,touch,"LArm","LeftFaceLed{}"))

        if lArmIsActive == 0:
            threadLArm.start()
        elif lArmIsActive == 2:
            pass

        if rArmIsActive == 0:
            threadRArm.start()
        elif rArmIsActive == 2:
            pass
        
        time.sleep(0.1) 


def touchRArm(leds,touch,sensor,led):
    global rArmIsActive
    rArmIsActive = 1
    while 1:

        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    rArmIsActive = 2
                    for i in range(8):
                            leds.fadeRGB(led.format(i+1), rainbow[i], speed)
                else:
                    rArmIsActive = 0
                    sys.exit()
                
                time.sleep(1)
                if rArmIsActive == 2:
                    while 1:
                        for i in range(8):
                            for j in range(8):
                                leds.fadeRGB(led.format(8-j), rainbow[i+j], rotate_speed)

                                status = touch.getStatus()
                                for e in status:
                                    if e[0] == sensor and e[1]==True:
                                        for i in range(8):
                                            leds.fadeRGB(led.format(i+1), white,speed)
                                        rArmIsActive = 0
                                        sys.exit()

def touchLArm(leds,touch,sensor,led):
    global lArmIsActive
    lArmIsActive = 1
    while 1:

        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    lArmIsActive = 2
                    for i in range(8):
                            leds.fadeRGB(led.format(8-i), rainbow[i], speed)
                else:
                    lArmIsActive = 0
                    sys.exit()
                
                time.sleep(1)
                if lArmIsActive == 2:
                    while 1:
                        for i in range(8):
                            for j in range(8):
                                leds.fadeRGB(led.format(j+1), rainbow[i+j], rotate_speed)

                                status = touch.getStatus()
                                for e in status:
                                    if e[0] == sensor and e[1]==True:
                                        for i in range(8):
                                            leds.fadeRGB(led.format(8-i), white,speed)
                                        lArmIsActive = 0
                                        return




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.253.22", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
