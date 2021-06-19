from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from eventmanager import binaryPredicate, changedValuePredicate
import time

class DialogManager:
    def __init__(self, robot_IP):
        self.asr = ALProxy("ALSpeechRecognition", robot_IP, 9559)
        self.tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
        self.memory = ALProxy("ALMemory",robot_IP,9559)
        self.touch = ALProxy("ALTouch", robot_IP, 9559)
    
    def askQ(self, question, answMap):
        self.tts.say(question)

        self._setVocab(answMap.keys())

        word = ""
        change = changedValuePredicate(lambda: self.memory.getData("WordRecognized")[1])
        while True:
            if not change():
                time.sleep(0.5)
                continue          
            word = self.memory.getData("WordRecognized")[0]
            if word not in answMap.keys():
                self.memory.insertData("WordRecognized", [0,0])
                self.tts.say("i dont understand, say this again ")
                continue
            break

        answMap[word]()
    
    def askBinaryQ(self, question, yesF, noF):
        self.tts.say(question)
        self._setVocab(["yes","no"])
        buttonY = binaryPredicate(lambda: self.touch.getStatus()[7][1], True)
        changedWord1 = changedValuePredicate(lambda: self.memory.getData("WordRecognized")[1])
        changedWord2 = changedValuePredicate(lambda: self.memory.getData("WordRecognized")[1])
        yesP = lambda: buttonY() or (changedWord1() and self.memory.getData("WordRecognized")[0] == "yes") 
        buttonN = binaryPredicate(lambda: self.touch.getStatus()[9][1], True)
        noP = lambda: buttonN() or (changedWord2() and self.memory.getData("WordRecognized")[0] == "no") 
        while True:
            if yesP():
                yesF()
                break
            if noP():
                noF()
                break
            time.sleep(0.1)



        
    def _setVocab(self, words):
        self.asr.subscribe("WordRecognized")
        self.memory.insertData("WordRecognized", [0,0])
        self.asr.pause(True)
        self.asr.setLanguage("English")
        self.asr.setVocabulary(words, False)
        self.asr.pause(False)

