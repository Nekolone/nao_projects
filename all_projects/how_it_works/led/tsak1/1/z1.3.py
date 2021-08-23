# -*- encoding: UTF-8 -*-

import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)
    
    leds.reset("AllLeds") 

    speed = 0.2
    color = 0x00ff00ff

    pulse = 0
    pulse_speed = 0.5

    while True:
        status = touch.getStatus()

        for e in status:
            if e[0] == "Head/Touch/Front" and e[1] == True:
                leds.fadeRGB("FaceLeds", color, speed)          #   для подключения второго глаза была изменена группа с 
                                                                #   "RightFaceLeds" на "FaceLeds", что позоляет изменять цвет всех глаз
                pulse = 0
            if e[0] == "Head/Touch/Rear" and e[1] == True:
                leds.fadeRGB("FaceLeds", 0x00ffffff, speed)
                pulse = 0
            
            if e[0] == "Head/Touch/Middle" and e[1] == True:
                pulse = 1

        if pulse == 1:
            leds.fadeRGB("FaceLeds", color, pulse_speed)
            leds.fadeRGB("FaceLeds", 0x00ffffff, pulse_speed)


main("192.168.253.22", 9559)    #Вызов функции main. main("ip робота", порт 9559)