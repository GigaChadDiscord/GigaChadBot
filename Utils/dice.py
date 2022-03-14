import random
class Dice():
    def __init__(self, sides):
        self.sides = sides
        self.values = []

    def roll(self, print=False):
        roll = random.randint(1, self.sides)
        if print:
            print(f"Rolled a {roll}")
        if roll <= len(self.values):
            return self.values[roll-1]
        return None

    def add_value(self, value):
        self.values.append(value)
    