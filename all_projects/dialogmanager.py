from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from eventmanager import binary_predicate, changed_value_predicate
from service import asr, tts, memory, touch
import time


class DialogManager:
    # def __init__(self, robot_IP):
    #     self.asr = ALProxy("ALSpeechRecognition", robot_IP, 9559)
    #     self.tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
    #     self.memory = ALProxy("ALMemory",robot_IP,9559)
    #     self.touch = ALProxy("ALTouch", robot_IP, 9559)

    def __init__(self):
        pass

    def askQ(self, question, answ_map):
        tts.say(question)

        self._set_vocab(answ_map.keys())

        word = ""
        change = changed_value_predicate(lambda: memory.getData("WordRecognized")[1])
        while True:
            if not change():
                time.sleep(0.5)
                continue
            word = memory.getData("WordRecognized")[0]
            if word not in answ_map.keys():
                memory.insertData("WordRecognized", [0, 0])
                tts.say("i dont understand, say this again ")
                continue
            break

        answ_map[word]()

    def ask_binary_q(self, question, yes_f, no_f):
        tts.say(question)
        self._set_vocab(["yes", "no"])
        button_y = binary_predicate(lambda: touch.getStatus()[7][1], True)
        changed_word1 = changed_value_predicate(lambda: memory.getData("WordRecognized")[1])
        changed_word2 = changed_value_predicate(lambda: memory.getData("WordRecognized")[1])
        yes_p = lambda: button_y() or (changed_word1() and memory.getData("WordRecognized")[0] == "yes")
        button_n = binary_predicate(lambda: touch.getStatus()[9][1], True)
        no_p = lambda: button_n() or (changed_word2() and memory.getData("WordRecognized")[0] == "no")
        while True:
            if yes_p():
                yes_f()
                break
            if no_p():
                no_f()
                break
            time.sleep(0.1)

    def _set_vocab(self, words):
        asr.subscribe("WordRecognized")
        memory.insertData("WordRecognized", [0, 0])
        asr.pause(True)
        asr.setLanguage("English")
        asr.setVocabulary(words, False)
        asr.pause(False)
