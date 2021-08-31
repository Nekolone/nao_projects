# -*- encoding: UTF-8 -*-

import time                     #   подключение библиотеки time

from naoqi import ALProxy       #   Подключение ALProxy
from naoqi import ALBroker      #   Подключение ALBroker
from naoqi import ALModule      #   Подключение ALModule

def main(robot_IP, robot_PORT=9559):    #   Обьявление функции main. Функция принимает два значения
                                        #   robot_ip и robot_port
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)        #   Подключение интерфейса ALLeds
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)      #   Подключение интерфейса ALTouch
    leds.reset("AllLeds")   #   Сброс LED по умолчанию
                            #   .reset("группа или конкретный светодиод")

    speed = 0.2             #   Скорость изменения цвета

    color = 0x00ff00ff      #   Добавление цвета в формате 0x00RRGGBB
    white = 0x00ffffff      #   где RR GG BB это 16-ричный код их цвета

    while True:             #   Бесконечный цикл

        status = touch.getStatus()  #   Получение состояний тактильных датчиков
        print status    
        for e in status:            #   Цикл, проходящий по массиву status
                                    #   данные передаются в переменную e и с каждой итерацией
                                    #   берется следующий по массиву элемент

            if e[0] == "Head/Touch/Front" and e[1] == True:     #   Проверка значения состояния датчика "Head/Touch/Front".
                                                                #   Если true (датчик активирован), выполнить действие

                leds.fadeRGB("RightFaceLeds", color, speed)     #   Включение всех ледов правого глаза. 
                                                                #   .fadeRGB("группа или конкретный светодиод", цвет, скорость изменения)

            if e[0] == "Head/Touch/Rear" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", white, speed)
       

main("192.168.253.38", 9559)    #Вызов функции main. main("ip робота", порт 9559)
