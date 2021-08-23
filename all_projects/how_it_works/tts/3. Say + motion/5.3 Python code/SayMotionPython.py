from naoqi import ALProxy

robot_IP= "192.168.253.85"  # Your NAO IP address 
PORT = 9559 # Port number for connecting to robot

motion = ALProxy("ALMotion",robot_IP, PORT)
tts=ALProxy("ALTextToSpeech",robot_IP, PORT)

motion.wakeUp() # waking NAO , he will get in standing position.
tts.say("Hello friend, how are you?") # Nao will say this line.
motion.moveTo(0.2, 0.0, 0.0) # Moving NAO(read description below).
motion.rest() # NAO gets in resting position (sits).
