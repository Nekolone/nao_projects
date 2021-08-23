#-*- coding: utf-8 -*-  # 
from naoqi import ALProxy

robot_IP= "192.168.253.85"  # Your NAO IP address 
PORT = 9559 # Port number for connecting to robot

mov = ALProxy("ALRobotPosture",robot_IP, PORT)
tts = ALProxy("ALAnimatedSpeech",robot_IP, PORT)
motion = ALProxy("ALMotion",robot_IP, PORT)

mov.goToPosture("Stand", 1.0)
    
tts.post.say("\\style=neutral\\ \\rspd=85\\ I'm going straight") 
motion.moveTo(0.4, 0, 0)
        
tts.post.say("\\style=neutral\\ \\rspd=85\\ I'm going left")
motion.moveTo(0, 0, 1.2)
motion.moveTo(0.4, 0, 0)
        
tts.post.say("\\style=neutral\\ \\rspd=85\\ I'm going right")
motion.moveTo(0, 0, -2.4)
motion.moveTo(0.4, 0, 0)
        
tts.post.say("\\style=neutral\\ \\rspd=85\\ I'm going back")
motion.moveTo(-0.4, 0, 0)
        
mov.goToPosture("Stand", 1.0)# NAO gets in standing position (default pose).
