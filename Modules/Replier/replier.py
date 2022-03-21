import random
from Utils.dice import Dice

class Replier:

    def __init__(self):
        self.TRIGGER_WORDS = []

        self.probability_of_triggered_reply = 30
        self.probability_of_normal_reply = 40
        self.probability_of_question_reply = 6

        self.dice_question = Dice(self.probability_of_question_reply)
        self.dice_question.add_value("Perhaps")

        self.dice_reply = Dice(self.probability_of_normal_reply)
        self.dice_reply.add_value("Your face is {}")
        self.dice_reply.add_value("Dint knew")
        self.dice_reply.add_value("Really?")
        self.dice_reply.add_value("sus")
        self.dice_reply.add_value("nou")

    def parse(self, message):
        if message.content:
            if message.content[-1] == '?':
                print(self.dice_question.roll())
            else:
                
                if any(t in message.content.lower() for t in self.TRIGGER_WORDS):
                    self.dice_reply.set_sides(self.probability_of_triggered_reply)
                print(self.dice_reply.roll().format(message.content))
