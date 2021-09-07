# coding=utf-8
import qi

ip = "192.168.252.250"


session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

"""
Подключение модулей для работы с интерфейсами нао

Вся информация по методам этих модулей искать нужно здесь
http://doc.aldebaran.com/2-8/naoqi/index.html
"""

# global anitext, asr, alife, posture, atts, video, tts, memory, motion, touch
anitext = session.service("ALAnimatedSpeech")
posture = session.service("ALRobotPosture")
memory = session.service("ALMemory")
motion = session.service("ALMotion")
alife = session.service("ALAutonomousLife")
video = session.service("ALVideoDevice")
touch = session.service("ALTouch")
atts = session.service("ALAnimatedSpeech")
asr = session.service("ALSpeechRecognition")
tts = session.service("ALTextToSpeech")
