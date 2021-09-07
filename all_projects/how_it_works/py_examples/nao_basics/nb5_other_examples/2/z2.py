# -*- encoding: UTF-8 -*-

import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)
    
    leds.reset("AllLeds") 

    green = 0x0000ff00
    yellow = 0x00ffff00
    red = 0x00ff0000

    while True:

        status = touch.getStatus()

        for e in status:

            if e[0] == "Head/Touch/Front" and e[1] == True:     #   Проверяет состояние сенсора Head/Touch/Front (передняя часть головы)
                leds.fadeRGB("AllLeds", green,0.2)              #   Окрашивает все цветные светодиоды в ЗЕЛЕНЫЙ цвет (0x0000ff00)

            if e[0] == "Head/Touch/Middle" and e[1] == True:    #   Проверяет состояние сенсора Head/Touch/Middle (центральная часть головы)
                leds.fadeRGB("AllLeds", yellow,0.2)             #   Окрашивает все цветные светодиоды в ЖЕЛТЫЙ цвет (0x00ffff00)

            if e[0] == "Head/Touch/Rear" and e[1] == True:      #   Проверяет состояние сенсора Head/Touch/Rear (задняя часть головы)
                leds.fadeRGB("AllLeds", red,0.2)                #   Окрашивает все цветные светодиоды в КРАСНЫЙ цвет (0x00ff0000)


main("192.168.253.22", 9559)