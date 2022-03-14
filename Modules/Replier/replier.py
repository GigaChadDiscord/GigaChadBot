import random
from Utils.dice import Dice

class Replier:
    TRIGGER_WORDS = []

    def __init__(self):
        self.probability_of_triggered_reply = 30
        self.probability_of_normal_reply = 40
        self.probability_of_question_reply = 6

        self.dice_question = Dice(self.probability_of_question_reply)
        self.dice_question.add_value("Perhaps")

    def parse(self, message):
        if message.content:
            if message.content[-1] == '?':
                self.dice_question.roll()
            else:
                dice_reply = Dice(self.probability_of_normal_reply)
                dice_reply.add_value(f"Your face is {message.content}")
                dice_reply.add_value("Dint knew")
                dice_reply.add_value("Really?")
                dice_reply.add_value("sus")
                dice_reply.add_value("nou")
                if any(t in message.content.lower() for t in self.TRIGGER_WORDS):
                    dice_reply.sides = self.probability_of_triggered_reply
                print(dice_reply.roll())
