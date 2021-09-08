# -*- encoding: UTF-8 -*-
import smtplib
import cv2 as cv
import numpy as np

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from _dialogmanager import *
from _eventmanager import *
from service import *

"""
Класс письма, в него добавляется вся необходимая для отправки сообщения информация
"""


class Email:
    def __init__(self, receiver_address, subject, mail_content, sender_address="tsinaolab@gmail.com",
                 sender_pass="#TSIRiga2018!"):
        self.receiver_address = receiver_address
        self.subject = subject
        self.mail_content = mail_content
        self.sender_address = sender_address
        self.sender_pass = sender_pass


"""
Запуск программы = main()

Происходит заполнение стартовой информации

(!!!ТУТ НУЖНО ВПИСАТЬ СВОЮ!!!)
"""


def start_pte():
    to = ["nikolafgh@gmail.com"]
    subject = "Hello from NAO"
    mail_content = """
    Hi, this is your photo
    """
    email = Email(to, subject, mail_content)
    photo_to_email(email)


"""
Нао встает, задает вопрос и ждет ответа
"""


def photo_to_email(email):
    motion.stopMove()
    posture.goToPosture("Stand", 0.4)
    alife.setState("safeguard")
    memory.insertData("WordRecognized", [0, 0])
    global loop
    loop = True
    global dialog_handler
    dialog_handler = DialogManager()
    """
    dialog_handler.ask_binary_q(вопрос, реакция на YES, реакция на NO)
    """
    dialog_handler.ask_binary_q("Do you want to take a picture?", lambda: takePhoto(email), no)
    while loop:
        dialog_handler.ask_binary_q("Do you want to take a picture again?", lambda: takePhoto(email), no)

    """
    Ниже выход из программы
    """
    asr.unsubscribe("WordRecognized")
    tts.say("It was great! Have a nice day!")
    alife.setState("solitary")


def no():
    global loop
    loop = False


"""
Получает фотографию, задает вопрос и ждет ответ
"""


def takePhoto(email):
    pic = get_photo()
    on_yes = lambda: send_email(prepared_email(pic, email))
    dialog_handler.ask_binary_q("Do you want to send to an email?", on_yes, lambda: True)


"""
Нао запускает отсчет, делает анимацию и фотографию.
"""


def get_photo():
    video_client = video.subscribeCamera("myCam", 0, 4, 13, 10)
    tts.say("Free photo to everyone in 5 sec")
    time.sleep(1)
    tts.say("4")
    time.sleep(1)
    tts.say("3")
    time.sleep(1)
    tts.say("2")
    time.sleep(1)
    tts.say("1")
    arg = "^start(animations/Stand/Waiting/TakePicture_1) Say cheese! ^wait(animations/Stand/Waiting/TakePicture_1)"
    Thread(target=anitext.say, args=[arg]).start()
    nao_image = video.getImageRemote(video_client)
    video.releaseImage(video_client)
    video.unsubscribe(video_client)
    image_width = nao_image[0]
    image_height = nao_image[1]
    array = nao_image[6]
    nparray = np.array(array)
    nparray = nparray.reshape((image_height, image_width, 3))
    _, im = cv.imencode('.jpeg', nparray)
    return im.tobytes()


"""
Готовит письмо к отправке
"""


def prepared_email(image, email):
    tts.say("ok sending")
    message = MIMEMultipart()
    message['Subject'] = email.subject
    message['From'] = email.sender_address
    message['To'] = ", ".join(email.receiver_address)
    message.preamble = email.subject
    message.attach(MIMEText(email.mail_content, "plain"))
    imge = MIMEImage(image, name="pic.jpg")
    imge.add_header('Content-Disposition', 'attachment; filename="pic.jpg"')
    message.attach(imge)
    email.message = message
    return email

"""
Подключается к серверам гугла и отправляет письмо с фотографией и вызывает завершение программы
"""
def send_email(email):
    email_session = smtplib.SMTP('smtp.gmail.com', 587)
    email_session.starttls()
    email_session.login(email.sender_address, email.sender_pass)
    email_session.sendmail(email.sender_address, email.receiver_address, email.message.as_string())
    tts.say("done")
    email_session.quit()


if __name__ == "__main__":
    start_pte()
