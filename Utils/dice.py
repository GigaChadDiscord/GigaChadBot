import random
import warnings

class Dice():
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        roll = random.randint(1, self.sides)
        print(f"Rolled a {roll}/{self.sides}")
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
        self.replies = replies

    def roll(self):
        if super().roll() == 1 and self.replies:
            return self.replies[random.randint(0, len(self.replies)-1)]
        return ""

    def get_replies(self):
        return self.replies
    
    def add_reply(self, reply):
        self.replies.append(reply)
        if len(self.replies) > self.sides:
            warnings.warn(f"Too many replies added to dice. Only {self.sides} replies will be used.")