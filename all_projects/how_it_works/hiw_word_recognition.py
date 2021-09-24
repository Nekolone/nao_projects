# -*- encoding: UTF-8 -*-
from _eventmanager import *
from service import *

"""
В хфриографе, при находжении человека будет выводить в чат распознанные слова. Также будет повторять их.
"""


def start_tracking():
    alife.setState("disabled")
    asr.subscribe("WordRecognized")
    motion.stopMove()

    """
    Пауза распознавания и добавление в словарь слов YES NO
    """
    asr.pause(True)
    asr.setLanguage("English")
    vocabulary = ["yes", "no"]
    asr.setVocabulary(vocabulary, False)
    asr.pause(False)

    """
    В getData("WordRecognized") хранится информация о последней попытке распознавания.
    Слово в ячейке 0, точность распознавания в ячейке 1
    """
    global em
    em = Eventloop()
    em.add_event(Event(starter_exit, [], get_stop_starter, single_use=True, threadable=True))
    em.add_event(Event(say_this, [lambda: memory.getData("WordRecognized")[0]],
                       changed_value_predicate(lambda: memory.getData("WordRecognized")[1]), threadable=True))
    em.start()
    em.join()

    asr.unsubscribe("WordRecognized")


def get_stop_starter():
    return touch.getStatus()[8][1]


def say_this(text):
    tts.say(text())


def starter_exit():
    global loop
    em.stop()
    loop = False
    motion.stopMove()
    posture.goToPosture("Stand", 0.4)


start_tracking()
