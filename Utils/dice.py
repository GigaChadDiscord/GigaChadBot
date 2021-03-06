import logging
import random
import warnings

logger = logging.getLogger('gigachad')


class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        roll = random.randint(1, self.sides)
        logger.debug(f"Rolled a {roll}/{self.sides}")
        return roll

    def set_sides(self, sides):
        self.sides = sides

    def get_sides(self):
        return self.sides


class BooleanDice(Dice):

    def roll(self):
        return super().roll() == 1


class ReplyDice(Dice):

    def __init__(self, sides, replies=[]):
        super().__init__(sides)
        self.replies = list(replies)

    def roll(self):
        if super().roll() == 1 and self.replies:
            reply = self.replies[random.randint(0, len(self.replies) - 1)]
            print(f"Replied with {reply}")
            return reply
        return ""

    def get_replies(self):
        return self.replies

    def add_reply(self, reply):
        self.replies.append(reply)
        if len(self.replies) > self.sides:
            warnings.warn(f"Too many replies added to dice. Only {self.sides} replies will be used.")
