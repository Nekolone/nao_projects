# -*- encoding: UTF-8 -*-

import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)            #   Подключение интерфейса для работы с диодами
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)          #   Подключение интерфейса для работы с тактильными сенсорами
    
    leds.reset("AllLeds") 

    green = 0x0000ff00          #   Добавление цвета в формате 0x00RRGGBB
    yellow = 0x00ffff00         #   где RR GG BB это 16-ричный код их цвета
    red = 0x00ff0000            #   
    mood_bg = 0x00000000

    speed = 0.1

    while True:

        status = touch.getStatus()      #   Получает массив с состояниями тактильных сенсоров

        for e in status:                #   Цикл, переберающий массив состояний тактильных сенсоров

            if e[0] == "Head/Touch/Front" and e[1] == True:     #   Проверяет состояние сенсора Head/Touch/Front (передняя часть головы)
                leds.fadeRGB("AllLeds", green, speed)              #   Окрашивает все цветные светодиоды в ЗЕЛЕНЫЙ цвет (0x0000ff00)
                leds.fadeRGB("FaceLed0", mood_bg, speed)
                leds.fadeRGB("FaceLed1", green, speed)
                leds.fadeRGB("FaceLed2", mood_bg, speed)
                leds.fadeRGB("FaceLed3", mood_bg, speed)
                leds.fadeRGB("FaceLed4", mood_bg, speed)
                leds.fadeRGB("FaceLed5", green, speed)
                leds.fadeRGB("FaceLed6", mood_bg, speed)
                leds.fadeRGB("FaceLed7", mood_bg, speed)

            if e[0] == "Head/Touch/Middle" and e[1] == True:    #   Проверяет состояние сенсора Head/Touch/Middle (центральная часть головы)
                leds.fadeRGB("AllLeds", yellow, speed)             #   Окрашивает все цветные светодиоды в ЖЕЛТЫЙ цвет (0x00ffff00)
                leds.fadeRGB("FaceLed0", mood_bg, speed)
                leds.fadeRGB("FaceLed1", mood_bg, speed)
                leds.fadeRGB("FaceLed2", yellow, speed)
                leds.fadeRGB("FaceLed3", mood_bg, speed)
                leds.fadeRGB("FaceLed4", mood_bg, speed)
                leds.fadeRGB("FaceLed5", mood_bg, speed)
                leds.fadeRGB("FaceLed6", yellow, speed)
                leds.fadeRGB("FaceLed7", mood_bg, speed)

            if e[0] == "Head/Touch/Rear" and e[1] == True:      #   Проверяет состояние сенсора Head/Touch/Rear (задняя часть головы)
                leds.fadeRGB("AllLeds", red, speed)                #   Окрашивает все цветные светодиоды в КРАСНЫЙ цвет (0x00ff0000)
                leds.fadeRGB("FaceLed0", mood_bg, speed)
                leds.fadeRGB("FaceLed1", mood_bg, speed)
                leds.fadeRGB("FaceLed2", mood_bg, speed)
                leds.fadeRGB("FaceLed3", red, speed)
                leds.fadeRGB("FaceLed4", mood_bg, speed)
                leds.fadeRGB("FaceLed5", mood_bg, speed)
                leds.fadeRGB("FaceLed6", mood_bg, speed)
                leds.fadeRGB("FaceLed7", red, speed)


main("192.168.253.22", 9559)