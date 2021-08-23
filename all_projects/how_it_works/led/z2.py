# -*- encoding: UTF-8 -*-

import time
import argparse

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

    while True:

        status = touch.getStatus()      #   Получает массив с состояниями тактильных сенсоров

        for e in status:                #   Цикл, переберающий массив состояний тактильных сенсоров

            if e[0] == "Head/Touch/Front" and e[1] == True:     #   Проверяет состояние сенсора Head/Touch/Front (передняя часть головы)
                leds.fadeRGB("AllLeds", green,0.2)              #   Окрашивает все цветные светодиоды в ЗЕЛЕНЫЙ цвет (0x0000ff00)

            if e[0] == "Head/Touch/Middle" and e[1] == True:    #   Проверяет состояние сенсора Head/Touch/Middle (центральная часть головы)
                leds.fadeRGB("AllLeds", yellow,0.2)             #   Окрашивает все цветные светодиоды в ЖЕЛТЫЙ цвет (0x00ffff00)

            if e[0] == "Head/Touch/Rear" and e[1] == True:      #   Проверяет состояние сенсора Head/Touch/Rear (задняя часть головы)
                leds.fadeRGB("AllLeds", red,0.2)                #   Окрашивает все цветные светодиоды в КРАСНЫЙ цвет (0x00ff0000)
                            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.253.66", help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)