# -*- encoding: UTF-8 -*-

import time
import threading
import random
import base64
import os
import httplib
import socket
import select
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# Если хотите скачать файл с гитхаба и не использовать библиотеку из проекта, нужно закоментировать это
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
sys.path.append(path + '\custom_lib')
# 

from threading import Thread
from eventmanager import *

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule



def eventRuka(robot_IP, robot_PORT=9559):

    global tts, memory, motion, alife, touch, vision
    
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    memory = ALProxy("ALMemory",robot_IP,robot_PORT)
    motion = ALProxy("ALMotion", robot_IP, robot_PORT)
    alife = ALProxy("ALAutonomousLife", robot_IP, robot_PORT)
    touch = ALProxy("ALTouch", robot_IP, robot_PORT)
    vision = ALProxy("ALPhotoCapture", robot_IP, robot_PORT)

    alife.setState("disabled")
    
    motion.stopMove()
    motion.wakeUp()

    vision.setResolution(2)
    vision.setPictureFormat("png")
    photoName = vision.takePicture("/opt/aldebaran/var/www/apps/", "image", True)
    # conn = httplib.HTTPConnection("192.168.252.226", 80)
    # conn.request("GET","/apps/image.png")
    # res = conn.getresponse().read()
    # picB64 = base64.b64encode(res)
    # print picB64

    address = ("192.168.252.226", 80)        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.sendall(b'GET /apps/image.png HTTP/1.1\r\nHOST: 192.168.252.226\r\n\r\n')

    reply = b''

    while select.select([s], [], [], 3)[0]:
        data = s.recv(2048)
        if not data: break
        reply += data

    headers =  reply.split(b'\r\n\r\n')[0]
    image = reply[len(headers)+4:]
    # save image
    f = open('image.png', 'wb')
    f.write(image)
    f.close()
    f = open('image.png', 'rb')
    # puctura = base64.b64encode(f.read())

    # mail = imaplib.IMAP4_SSL('imap.gmail.com')
    # mail.login("tsinaolab@gmail.com","#TSIRiga2018!")
    
    # Create a secure SSL context
    mail_content = '''Hello,
    This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
    Thank You
    '''
    sender_address = "tsinaolab@gmail.com"
    receiver_address = "ljaksa.i@tsi.lv"
    sender_pass = "#TSIRiga2018!"
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
    message = MIMEMultipart("alternative")
    part = MIMEText("hallo", "plain")
    msg_image = MIMEImage(f.read())
    # msg_image.add_header('Content-ID', '<{0}>'.format(image['id']))
    message.attach(msg_image)


    #The body and the attachments for the mail
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


    global loop
    loop = True


    tts.say("It was great! Have a nice day!")
    alife.setState("interactive")



def naoExit():
    global loop
    eventHandler.stop()
    loop=False
    motion.stopMove()
    posture.goToPosture("Stand",0.4)



eventRuka("192.168.252.226", 9559)
# eventRuka("192.168.253.155", 9559)
# eventRuka("192.168.253.155", 9559)
# eventRuka("192.168.253.80", 9559)
# eventRuka("NaoThree.local", 9559)
