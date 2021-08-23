# coding=utf-8
import qi

# ip = "192.168.252.226"
ip = "192.168.252.250"
# ip = "192.168.253.155"
# ip = "192.168.252.247"
# ip = "192.168.253.68"


session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")

global anitext, asr, alife, posture, atts, video, tts, memory, motion, touch
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
