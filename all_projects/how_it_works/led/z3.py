# -*- encoding: UTF-8 -*-

import time
import argparse

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)
    
    leds.reset("AllLeds") 

    color1 = 0x00ffff00
    color2 = 0x00ff00ff
    white = 0x00ffffff

    speed = 0.2

    while True:

        status = touch.getStatus()

        for e in status:

            if e[0] == "LFoot/Bumper/Left" and e[1] == True:
                leds.fadeRGB("LeftFaceLeds", color1, speed)
            elif e[0] == "LFoot/Bumper/Right" and e[1] == True:
                leds.fadeRGB("LeftFaceLeds", color1, speed)

            if e[0] == "RFoot/Bumper/Left" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", color2, speed)
            elif e[0] == "RFoot/Bumper/Right" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", color2, speed)

            if e[0] == "LArm" and e[1] == True:
                leds.fadeRGB("LeftFaceLeds", white, speed)

            if e[0] == "RArm" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", white, speed)
            

            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.253.66", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)