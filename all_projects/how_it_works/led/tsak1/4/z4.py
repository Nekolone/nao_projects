# -*- encoding: UTF-8 -*- 

import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

rainbow=[       #   Обьявление массива кодов разных цветов
    0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff,
    0x00ff0000, 0x00ff7f00, 0x00ffff00, 0x007fff00, 0x0000ffff, 0x000000ff, 0x007f00ff, 0x00ff00ff] 

white = 0x00ffffff

speed = 0.2
rotate_speed = 0.01

def main(robot_IP, robot_PORT=9559):
    
    leds = ALProxy("ALLeds",robot_IP,robot_PORT)
    touch = ALProxy("ALTouch",robot_IP,robot_PORT)
    
    leds.reset("AllLeds") 

    while True:
        
        touchLArm(leds,touch,"LArm","LeftFaceLed{}")

        time.sleep(0.1)                 #   Ожидаем 0.1 секунду


def touchLArm(leds,touch,sensor,led):   #   Обьявление функции touchLArm, с получаемыми параметрами leds,touch,sensor,led
            # sensor = "LArm"
            # led = "LeftFaceLed{}"
    
    while 1:

        status = touch.getStatus()
        for e in status:
            if e[0] == sensor:
                if e[1]==True:
                    for i in range(8):      #   окраска ледов в цикле, постепенно
                            leds.fadeRGB(led.format(8-i), rainbow[i], speed)
                else:
                    return      #   выход и завершение функции в случае отсутствия активных датчиков
                
                time.sleep(1)
                while 1:
                    for i in range(8):          #   двойной цикл для создания бегущего огня
                        for j in range(8):
                            leds.fadeRGB(led.format(j+1), rainbow[i+j], rotate_speed)

                            status = touch.getStatus()
                            for e in status:    #   в случае повторного нажатия на датчик, запускает цикл окраски глаза в обычный цвет и выхода из функции
                                if e[0] == sensor and e[1]==True:
                                    for i in range(8):
                                        leds.fadeRGB(led.format(8-i), white,speed)
                                    return


main("192.168.253.66", 9559)