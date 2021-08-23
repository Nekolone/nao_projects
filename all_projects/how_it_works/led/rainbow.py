# -*- encoding: UTF-8 -*- 

import sys
import time
import qi
import argparse
import threading
# import thread

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from threading import Thread
import argparse

rainbow=[0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff,0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff] 

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)


    alife = ALProxy("ALAutonomousLife",robot_IP,robot_PORT)
    alife.setState("disabled")

    posture = ALProxy("ALRobotPosture",robot_IP,robot_PORT)
    posture.goToPosture("Stand",0.5)

    global headIsActive, handIsActive
    headIsActive, handIsActive = 0,0

  



    while True:
        threadHead = Thread(target=touchHead, args=(leds,touch,"Head/Touch/Middle","R",8,"RightFaceLed{}"))
        threadHand = Thread(target=touchHand, args=(leds,touch))



        if headIsActive == 0:
            threadHead.start()
        elif headIsActive == 2:
            headIsActive = 0
            leds.on("RightFaceLeds")

        time.sleep(0.05)

        if handIsActive == 0:
            threadHand.start()
        elif handIsActive == 2:
            handIsActive = 0
            leds.on("LeftFaceLeds")
        
        time.sleep(0.05)
            
        # if checkHand.is_alive()==False:

        
        # if checkHead.is_alive()==False:
        #     checkHead.start()

        # if active_count == 0:
        #     leds.on("FaceLeds")
        
    



def touchHead(leds,touch,sensor,RL,loop,led):
    global headIsActive
    headIsActive = 1
    while 1:            
        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    headIsActive = 3
                    for i in range(8):
                        leds.fadeRGB(led.format(i+1), rainbow[i],0.2)
                else:
                    headIsActive = 2
                    sys.exit()

                hexit = lambda touch,sensor: headExit(touch,sensor) 
                # rotate(leds,touch,hexit,sensor,RL,loop,led)
                
def touchHand(leds,touch):
    global handIsActive
    handIsActive = 1
    rainbow=[0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff,0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff] 
    while 1:            
        status = touch.getStatus()
        for e in status:
            if e[0] == "RHand/Touch/Back":
                if e[1]==True:
                    handIsActive = 3
                    for i in range(8):
                        leds.fadeRGB("LeftFaceLed{}".format(8-i), rainbow[i],0.2)
                else:
                    handIsActive = 2
                    sys.exit()
                
                if handIsActive == 3:
                    while 1:

                        for i in range(8):
                            for j in range(8):
                                leds.fadeRGB("LeftFaceLed{}".format(8-j), rainbow[i+j],0.01)
                                status = touch.getStatus()
                                
                                for e in status:
                                    if e[0] == "RHand/Touch/Back" and e[1]==True:
                                        leds.on("LeftFaceLeds")
                                        handIsActive = 2
                                        time.sleep(2)
                                        sys.exit()


def rotate(leds,touch,funcR,sensor,RL,loop,led):
    while 1:    
        for i in range(loop):
            for j in range(loop):
                if RL == "R":
                    leds.fadeRGB(led.format(j+1), rainbow[i+j],0.01)
                else:
                    leds.fadeRGB(led.format(loop-j), rainbow[i+j],0.01)

                status = touch.getStatus()

                funcR(touch,sensor)

def headExit(touch,sensor):
    global headIsActive
    status = touch.getStatus()
    for e in status:
        if e[0] == sensor and e[1]==True:
            headIsActive = 2
            time.sleep(2)
            sys.exit()




                
                
        
    



                    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.253.66", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
