
#-*- coding: utf-8 -*-     # This way of specifying the encoding of a Python file
from naoqi import ALProxy  # Getting ALProxy module

robot_IP= "192.168.253.85"  # Your NAO IP address 
PORT = 9559 # Port number for connecting to robot

tts = ALProxy("ALTextToSpeech",robot_IP,PORT) # create proxy on TextToSpeech
tts.say("Hello")  # Saying hello
