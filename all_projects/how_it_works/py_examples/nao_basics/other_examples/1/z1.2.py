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
    white = 0x00ffffff

    pulse = 0           #   Состояние пульсации глаз. 0-выклюбчена. 1-включена
    pulse_speed = 0.5   #   Скорость пульсации глаз

    while True:
        status = touch.getStatus()

        for e in status:
            if e[0] == "Head/Touch/Front" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", color, speed)
                pulse = 0                                       #   Выключение пульсации при нажатии "Head/Touch/Front"
            if e[0] == "Head/Touch/Rear" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", white, speed)
                pulse = 0                                       #   Выключение пульсации при нажатии "Head/Touch/Rear"
            
            if e[0] == "Head/Touch/Middle" and e[1] == True:
                pulse = 1                                       #   Включение пульсации при нажатии "Head/Touch/Middle"

        if pulse == 1:                                          #   Проверка состояния значения переменной pulse
            leds.fadeRGB("RightFaceLeds", color, pulse_speed)   #   Включение светодиода цветом color
            leds.fadeRGB("RightFaceLeds", white, pulse_speed)   #   Включение светодиода цветом white


main("192.168.253.22", 9559)    #Вызов функции main. main("ip робота", порт 9559)