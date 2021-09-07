#-*- coding: utf-8 -*-  # 
from naoqi import ALProxy

robot_IP= "192.168.253.85"  # Your NAO IP address 
PORT = 9559 # Port number for connecting to robot

tts=ALProxy("ALTextToSpeech",robot_IP, PORT) # Creates a proxy on the text-to-speech module

tts.setParameter("speed", 50) # making nao speak at certain speed
tts.setParameter("pitchShift", 0.8) # making nao speak at certain pitch
tts.say("Hello \\pau=1000\\ how are you?") #making nao speak with pause of 1 second
