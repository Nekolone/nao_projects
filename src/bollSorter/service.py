import qi

import eventmanager

ip = "192.168.252.226"
# ip = "192.168.253.155"
# ip = "192.168.253.68"

global video, tts, memory, motion, alife, posture, atts, touch

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")


video = session.service( "ALVideoDevice" )   
tts = session.service( "ALTextToSpeech" )
memory = session.service( "ALMemory" )
motion = session.service( "ALMotion" )
alife = session.service( "ALAutonomousLife" )
posture = session.service( "ALRobotPosture" )
atts = session.service( "ALAnimatedSpeech" )
touch = session.service( "ALTouch" )


