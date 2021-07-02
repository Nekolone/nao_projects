import win32com.client as win32
import time
import qi

from pptx import Presentation

def main(session):
    tts = session.service("ALTextToSpeech")
    # tts.setVoice("Alyona22Enhanced")
    tts.say("HELLO")
    time.sleep(1)
    tts.say("\\vct=100\\HELLO")
    time.sleep(1)
    tts.say("\\vct=50\\HELLO")
    time.sleep(1)
    tts.say("\\rspd=100\\HELLO")
    time.sleep(1)
    tts.say("\\rspd=50\\HELLO")
    time.sleep(1)
    tts.say("\\vol=100\\HELLO")
    time.sleep(1)
    tts.say("\\vol=50\\HELLO")
    time.sleep(1)
    tts.say("\\mrk=100\\HELLO")
    tts.say("\\mrk=50\\HELLO")
    tts.say("\\Ищгтв=50\\HELLO")
    tts.say("\\mrk=50\\HELLO")
   
    



if __name__ == "__main__":
    session = qi.Session()
    # session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
    # session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
    # session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
    session.connect("tcp://" + "192.168.253.155" + ":" + "9559")
    main(session)