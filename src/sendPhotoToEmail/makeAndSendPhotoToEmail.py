# -*- encoding: UTF-8 -*-

# import threading
# import random
# import base64
# import os
# import httplib
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


# Если хотите скачать файл с гитхаба и не использовать библиотеку из проекта, нужно закоментировать это
# import sys
# path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
# sys.path.append(path + '\custom_lib')
# from eventmanager import *
# 

# from threading import Thread



def makeAndSendPhotoToEmail(
    robot_IP, robot_PORT=9559, 
    receiver_address="nikolafgh@gmail.com",
    sender_address = "tsinaolab@gmail.com", sender_pass = "#TSIRiga2018!", 
    resol = 4, picFormat = "jpg",
    subject="Hello from NAO", mail_content="Hi, this is your photo"):

    global tts, memory, motion, alife, touch, vision
    
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    memory = ALProxy("ALMemory",robot_IP,robot_PORT)
    motion = ALProxy("ALMotion", robot_IP, robot_PORT)
    # alife = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
    touch = ALProxy("ALTouch", robot_IP, robot_PORT)
    vision = ALProxy("ALPhotoCapture", robot_IP, robot_PORT)
    # vision = ALProxy("ALVideoDevice", robot_IP, robot_PORT)

    sendEmail(**preparedEmail(getPhoto(resol, picFormat), receiver_address, subject, mail_content, sender_address, sender_pass))

    tts.say("It was great! Have a nice day!")
    # alife.setState("interactive")

def getPhoto(resol, picFormat):
    vision.setResolution(resol)
    vision.setPictureFormat(picFormat)
    vision.takePicture("/opt/aldebaran/var/www/apps/", "image", True)
 
    address = ("192.168.252.226", 80)        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.sendall(b'GET /apps/image.'+ picFormat + b' HTTP/1.1\r\nHOST: 192.168.252.226\r\n\r\n')
    reply = b''

    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data: break
        reply += data

    headers =  reply.split(b'\r\n\r\n')[0]
    image = reply[len(headers)+4:]
    return image

def preparedEmail(image, receiver_address, subject, mail_content, sender_address, sender_pass):

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_address
    message['To'] = receiver_address
    message.preamble = subject
    message.attach(MIMEText(mail_content, "plain"))
    message.attach(MIMEImage(image))
    return {"receiver_address":receiver_address, "message":message, "sender_address":sender_address, "sender_pass":sender_pass}

def sendEmail(receiver_address, message, sender_address, sender_pass):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    session.sendmail(sender_address, receiver_address, message.as_string())
    session.quit()


makeAndSendPhotoToEmail(
    robot_IP = "192.168.252.226", robot_PORT=9559, 
    receiver_address="nikolafgh@gmail.com",
    sender_address = "tsinaolab@gmail.com", sender_pass = "#TSIRiga2018!", 
    resol = 4, picFormat = "jpg",
    subject="A test mail sent by Python. It has an attachment.", 
    mail_content='''Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You''')
# eventRuka("192.168.253.155", 9559)
# eventRuka("192.168.253.155", 9559)
# eventRuka("192.168.253.80", 9559)
# eventRuka("NaoThree.local", 9559)
