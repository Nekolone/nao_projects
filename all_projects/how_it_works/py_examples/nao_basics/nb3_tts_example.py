# coding=utf-8
import qi

ip = "192.168.252.250"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

"""
Модуль для озвучивания введенного текста

http://doc.aldebaran.com/2-8/naoqi/audio/altexttospeech.html
"""

tts = session.service("ALTextToSpeech")


def main():
    tts.say("Hi Mark!")
    # tts.........


if __name__ == '__main__':
    main()
