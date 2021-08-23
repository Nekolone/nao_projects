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

    speed = 0.2
    color = 0x00ff00ff
    white = 0x00ffffff

    pulse = 0
    pulse_speed = 0.5

    while True:
        status = touch.getStatus()

        for e in status:
            if e[0] == "Head/Touch/Front" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", color, speed)
                pulse = 0
            if e[0] == "Head/Touch/Rear" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", white, speed)
                pulse = 0
            
            if e[0] == "Head/Touch/Middle" and e[1] == True:
                pulse = 1

        if pulse == 1:
            leds.fadeRGB("RightFaceLeds", color, pulse_speed)
            leds.fadeRGB("RightFaceLeds", white, pulse_speed)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.253.66", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)
