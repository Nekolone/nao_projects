# coding=utf-8
import qi
import time

ip = "192.168.252.250"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

"""
По нажатию на кнопку головы загораются глаза


http://doc.aldebaran.com/2-8/naoqi/sensors/altouch.html
http://doc.aldebaran.com/2-8/family/nao_technical/contact-sensors_naov6.html


http://doc.aldebaran.com/2-8/naoqi/sensors/alleds.html
http://doc.aldebaran.com/2-8/family/nao_technical/leds_naov6.html#naov6-led
"""

leds = session.service("ALLeds")
touch = session.service("ALTouch")


def main():
    leds.reset("AllLeds")

    speed = 2
    color = 0x00ff00ff
    white = 0x00ffffff

    while True:
        status = touch.getStatus()
        print status
        time.sleep(2)

        for e in status:
            if e[0] == "Head/Touch/Front" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", color, speed)
            if e[0] == "Head/Touch/Rear" and e[1] == True:
                leds.fadeRGB("RightFaceLeds", white, speed)


if __name__ == '__main__':
    main()
