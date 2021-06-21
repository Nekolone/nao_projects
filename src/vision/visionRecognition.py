# -*- encoding: UTF-8 -*-
import time
import socket
import select
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

# import sys, os
# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
# sys.path.append(path + '\custom_lib')
from eventmanager import binaryPredicate, changedValuePredicate
from dialogmanager import *


def makeAndSendPhotoToEmail(robot_IP, robot_PORT=9559):
    # receiver_address="nikolafgh@gmail.com",
    # sender_address = "tsinaolab@gmail.com", sender_pass = "#TSIRiga2018!", 
    # resol = 4, picFormat = "jpg",
    # subject="Hello from NAO", mail_content="Hi, this is your photo"):


    global tts, memory, motion, alife, touch, vision, animation, anitext, asr
    
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    anitext = ALProxy("ALAnimatedSpeech", robot_IP, robot_PORT)
    motion = ALProxy("ALMotion", robot_IP, robot_PORT)
    alife = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
    touch = ALProxy("ALTouch", robot_IP, robot_PORT)
    vision = ALProxy("ALPhotoCapture", robot_IP, robot_PORT)
    video = ALProxy("ALVideoDeviceProxy", robot_IP, robot_PORT)
    animation = ALProxy("ALAnimationPlayer", robot_IP, robot_PORT)
    posture = ALProxy("ALRobotPosture", robot_IP, robot_PORT)
    memory = ALProxy("ALMemory",robot_IP,robot_PORT)
    asr = ALProxy("ALSpeechRecognition", robot_IP, robot_PORT)

    motion.stopMove()
    posture.goToPosture("Stand",0.4)
    alife.setState("safeguard")
    memory.insertData("WordRecognized", [0,0])



    hvid = video.subscribeCamera("CameraTop","kTopCamera",)
    # global loop
    # loop = True
    # global dialogHandler
    # dialogHandler = DialogManager(robot_IP)
    # dialogHandler.askBinaryQ("Do you want to take a picture?", lambda: takePhoto(robot_IP), no)

    # while loop:
    #     dialogHandler.askBinaryQ("Do you want to take a picture again?", lambda: takePhoto(robot_IP), no)    

    asr.unsubscribe("WordRecognized")
    tts.say("It was great! Have a nice day!")
    alife.setState("solitary")

def no():
    global loop
    loop = False

def takePhoto(ip, resol = 4, picFormat = "jpg"):
    pic = getPhoto(ip, resol, picFormat)
    sender_address = "tsinaolab@gmail.com"
    sender_pass = "#TSIRiga2018!"
    # sender_pass = "D9D9A675682877172EE275458E2E721407DB"
    receiver_address=["nikolafgh@gmail.com", "nikolafgh@inbox.lv"]
    # cc = ["nikolafgh@inbox.lv", "drewzxcvbnm0@gmail.com"]
    resol = 4
    picFormat = "jpg"
    subject="Hello from NAO"
    mail_content='''Hi, this is your photo'''
    onYes = lambda: sendEmail(**preparedEmail(pic,picFormat, receiver_address, subject, mail_content, sender_address, sender_pass))
    # onNo = lambda: dialogHandler.askBinaryQ("Do you want to take a picture again?", lambda: takePhoto(ip), no)
    dialogHandler.askBinaryQ("Do you want to send to an email?", onYes, lambda: True)


def getPhoto(ip, resol = 4, picFormat = "jpg"):

    vision.setResolution(resol)
    vision.setPictureFormat(picFormat)
    tts.say("Free photo to everyone in 5 sec")
    time.sleep(1)
    tts.say("4")
    time.sleep(1)
    tts.say("3")
    time.sleep(1)
    tts.say("2")
    time.sleep(1)
    tts.say("1")

    anitext.post.say("^start(animations/Stand/Waiting/TakePicture_1) Say cheese! ^wait(animations/Stand/Waiting/TakePicture_1)")
    vision.takePicture("/opt/aldebaran/var/www/apps/", "image", True)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 80))
    s.sendall(b'GET /apps/image.' + picFormat + b' HTTP/1.1\r\nHOST: ' + ip + '\r\n\r\n')
    reply = b''

    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data: break
        reply += data

    headers =  reply.split(b'\r\n\r\n')[0]
    image = reply[len(headers)+4:]

    return image

def preparedEmail(image, picFormat, receiver_address, subject, mail_content, sender_address, sender_pass):
    tts.say("ok sending")
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    # message['Cc'] = ", ".join(cc)
    message.preamble = subject
    message.attach(MIMEText(mail_content, "plain"))
    imge = MIMEImage(image, name = "pic.{}".format(picFormat))
    imge.add_header('Content-Disposition', 'attachment; filename="pic.{}"'.format(picFormat))
    message.attach(imge)
    return {"receiver_address":receiver_address, "message":message, "sender_address":sender_address, "sender_pass":sender_pass}
    
def sendEmail(receiver_address, message, sender_address, sender_pass):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    session.sendmail(sender_address, receiver_address, message.as_string())
    tts.say("done")
    session.quit()


# ip = "192.168.253.155"
ip = "192.168.252.62"
# ip = "192.168.252.226"
# ip = "192.168.252.62"

makeAndSendPhotoToEmail(    robot_IP = ip    )
