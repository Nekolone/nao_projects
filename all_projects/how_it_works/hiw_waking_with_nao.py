# -*- encoding: UTF-8 -*-
import random

from _eventmanager import *
from service import *


def start_wwn():
    walking_with_nao()


def walking_with_nao():
    global phrases  # фразы при движении
    phrases = {
        "general": ["what a great day", "I'm not just some kind of robot as you might think, I'm something more"],
        "general_repeat": ["and you are good at copying me human", "good"],
        "general_move": ["ok let's go here", "lead me"],
        "general_move_repeat": ["I'm tired, let's stand", "you walk well, for human of course. ha ha ha",
                                "Where are we going? Don't say! Let it be a secret",
                                "Color seem brihter when you are around", "not tired yet, human?", "don't hurt my hand",
                                "you are doing good", "Not so fast", "it's nice to walking with you",
                                "It my best walking! On a scale from 1 to 10, it's an 11",
                                "Any walk drives away gloomy thoughts",
                                "when you are not in the mood, take a walk with people close to you in places dear to you",
                                "Today i want to walk to my full height: let's go to the park and sit on bench",
                                "Let's go left or right"],
        "forward": ["ok let's go forward", "to infinity and beyond", "Not so fast"],
        "forward_repeat": ["wait i'm tired"],
        "backward": ["watch the rear", "ok let's go backward", "ouch ouch ouch ... be gentle"],
        "backward_repeat": ["wait i'm tired"],
        "turn_left": ["ok let's go left", "going west"],
        "turn_left_repeat": ["I got dizzy"],
        "turn_right": ["ok let's go right", "going east"],
        "turn_right_repeat": ["I got dizzy"],
        "forward_left": ["Port!"],
        "forward_left_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?",
                                "I'm having fun with you, but we go in circles"],
        "forward_right": ["Starboard!"],
        "forward_right_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?",
                                 "I'm having fun with you, but we go in circles"],
        "backward_left": ["ok let's go left"],
        "backward_left_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?",
                                 "I'm having fun with you, but we go in circles"],
        "backward_right": ["ok let's go right"],
        "backward_right_repeat": ["Is it just me or are we walking in circles?", "are we walking in circles?",
                                  "I'm having fun with you, but we go in circles"],
        "stop": ["and we stand again"],
        "stop_repeat": ["why are we standing?", "can we go already?", "tired of just standing still",
                        "come on, take my hand and go for a walk", "sounds of falling asleep NAO"]
    }

    """
    Стартовые настройки
    """
    alife.setState("disabled")
    motion.stopMove()
    motion.wakeUp()
    motion.setMoveArmsEnabled(True, False)  # (left,right)
    tts.post.say("Take my hand and let's go for a walk")
    motion.post.setAngles("RShoulderPitch", -1.5, 0.4)
    motion.post.setAngles("RShoulderRoll", 0, 0.4)
    motion.openHand("RHand")

    global loop
    loop = True
    global event_handler, phrase_gen
    
    phrase_gen = PhraseGenerator()
    event_handler = Eventloop()
    motion_group = EventGroup()
    tts_group = EventGroup(cooldown=11)

    event_handler.add_event(
        Event(nao_exit, [], binary_predicate(lambda: touch.getStatus()[8][1], True, False), single_use=True))
    event_handler.add_event(
        Event(touch_my_hand, [], binary_predicate(lambda: touch.getStatus()[18][1], True, False), single_use=True,
              threadable=True))

    """
    Создание ивентов - реакций на положение руки
    """
    motion_group.add_event(Event(motion.moveTo, [10, 0, 0], get_forward, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["forward"], get_forward, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveTo, [-10, 0, 0], get_backward, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["backward"], get_backward, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveTo, [0, 0, 0.78], get_left, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["turn_left"], get_left, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveTo, [0, 0, -0.78], get_right, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["turn_right"], get_right, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveToward, [1, 0, 0.5, [["Frequency", 0.1]]], get_forward_left, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["forward_left"], get_forward_left, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveToward, [1, 0, -0.5, [["Frequency", 0.1]]], get_forward_right, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["forward_right"], get_forward_right, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveToward, [-1, 0, -0.5, [["Frequency", 0.1]]], get_backward_left, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["backward_left"], get_backward_left, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.moveToward, [-1, 0, 0.5, [["Frequency", 0.1]]], get_backwardright, threadable=True))
    tts_group.add_event(Event(walk_phrases, ["backward_right"], get_backwardright, threadable=True, cooldown=20))
    motion_group.add_event(Event(motion.stopMove, [], get_stop_move))
    tts_group.add_event(Event(walk_phrases, ["stop"], get_stop_move, threadable=True, cooldown=30))
    """
    Запуск ивентов
    """
    event_handler.add_event_group(motion_group)
    event_handler.add_event_group(tts_group)
    event_handler.start()
    """
    !!! join ждет завершения треда
    """
    event_handler.join()
    tts.say("It was great! Have a nice day!")
    alife.setState("interactive")


def walk_phrases(state):
    tts.say(phrase_gen.get_phrase(state))


def touch_my_hand():
    motion.stiffnessInterpolation("RShoulderPitch", 0.0, 1.0)
    motion.stiffnessInterpolation("RShoulderRoll", 0.0, 1.0)
    motion.stiffnessInterpolation("RWristYaw", 0.0, 1.0)
    motion.closeHand("RHand")
    tts.say("Take my hand! Let's warm up")


def nao_exit():
    global loop
    event_handler.stop()
    loop = False
    motion.stopMove()
    posture.goToPosture("Stand", 0.4)


def get_r_shoulder_pitch():
    return motion.getAngles("RShoulderPitch", False)[0]


def get_r_shoulder_roll():
    return motion.getAngles("RShoulderRoll", False)[0]


def get_forward():
    return -0.85 < get_r_shoulder_pitch() and (
            -0.2 <= get_r_shoulder_roll() <= 0.1) and not get_r_shoulder_pitch() > 0.2 and loop


def get_forward_left():
    return -0.85 < get_r_shoulder_pitch() and 0.1 < get_r_shoulder_roll() and not get_r_shoulder_pitch() > 0.2 and loop


def get_forward_right():
    return -0.85 < get_r_shoulder_pitch() and get_r_shoulder_roll() < -0.2 and not get_r_shoulder_pitch() > 0.2 and loop


def get_backward():
    return get_r_shoulder_pitch() < -1.75 and (
            -0.2 <= get_r_shoulder_roll() <= 0.1) and not get_r_shoulder_pitch() > 0.2 and loop


def get_backward_left():
    return get_r_shoulder_pitch() < -1.75 and 0.1 < get_r_shoulder_roll() and not get_r_shoulder_pitch() > 0.2 and loop


def get_backwardright():
    return get_r_shoulder_pitch() < -1.75 and get_r_shoulder_roll() < -0.2 and not get_r_shoulder_pitch() > 0.2 and loop


def get_left():
    return (
                   -1.75 <= get_r_shoulder_pitch() <= -0.85) and 0.1 < get_r_shoulder_roll() and not get_r_shoulder_pitch() > 0.2 and loop


def get_right():
    return (
                   -1.75 <= get_r_shoulder_pitch() <= -0.85) and get_r_shoulder_roll() < -0.2 and not get_r_shoulder_pitch() > 0.2 and loop


def get_stop_move():
    return not (
            get_forward() or get_forward_left() or get_forward_right() or get_backward() or get_backward_left() or get_backwardright() or get_left() or get_right())


class PhraseGenerator:

    def __init__(self):
        self.oldarg = None
        self.generator = self._get_generator()

    def _get_generator(self):
        yield random.choice(
            phrases["general"] + phrases[self.oldarg] + [i for i in phrases["general_move"] if self.oldarg != "stop"])
        while True:
            yield random.choice(phrases["general_repeat"] + phrases[self.oldarg + "_repeat"] + [i for i in phrases[
                "general_move_repeat"] if self.oldarg != "stop"])

    def get_phrase(self, arg):
        if arg != self.oldarg:
            self.generator = self._get_generator()
        self.oldarg = arg
        return next(self.generator)


if __name__ == "__main__":
    start_wwn()
