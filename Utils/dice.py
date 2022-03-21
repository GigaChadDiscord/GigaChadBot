import random
import warnings

class Dice():
    def __init__(self, sides, probability=True):
        self.sides = sides
        if not probability:
            self.values = list(range(1, sides+1))
        else:
            self.values = []

    def roll(self):
        roll = random.randint(1, self.sides)
        print(f"Rolled a {roll}/{self.sides}")
        if roll <= len(self.values):
            return self.values[roll-1]
        return None

    def get_values(self):
        return self.values
    
    def add_value(self, value):
        self.values.append(value)
        if len(self.values) > self.sides:
            warnings.warn(f"Too many values added to dice. Only {self.sides} values will be used.")

    def set_sides(self, sides):
        self.sides = sides

    def get_sides(self):
        return self.sides
    