#-*- coding: utf-8 -*-  # 
from naoqi import ALProxy

robot_IP= "192.168.253.85"  # Your NAO IP address 
PORT = 9559 # Port number for connecting to robot

mov = ALProxy("ALRobotPosture",robot_IP, PORT)
tts = ALProxy("ALAnimatedSpeech",robot_IP, PORT)



tts.say(" Hello, my best friend! ^run(System/animations/Stand/Exclamation/NAO/Center_Strong_EXC_06)")

mov.goToPosture("Stand", 1.0 )