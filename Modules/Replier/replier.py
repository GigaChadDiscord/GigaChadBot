import logging
import random
from Utils.dice import Dice, BooleanDice, ReplyDice

logger = logging.getLogger('gigachad')


class Replier:

    def __init__(self):
        self.TRIGGER_WORDS = []

        self.probability_of_triggered_reply = 20
        self.probability_of_normal_reply = 30
        self.probability_of_question_reply = 5

        self.dice_question = ReplyDice(self.probability_of_question_reply)
        self.dice_question.add_reply("Perhaps")

        self.dice_reply = ReplyDice(self.probability_of_normal_reply)
        self.dice_reply.add_reply("Your face is {}")
        self.dice_reply.add_reply("Dint knew")
        self.dice_reply.add_reply("Really?")
        self.dice_reply.add_reply("sus")
        self.dice_reply.add_reply("nou")
        logger.info("Replier initialized")

    def parse(self, message):
        if message.content:
            if message.content[-1] == '?':
                return self.dice_question.roll()
            else:
                if any(t in message.content.lower() for t in self.TRIGGER_WORDS):
                    self.dice_reply.set_sides(self.probability_of_triggered_reply)
                return self.dice_reply.roll().format(message.content)
