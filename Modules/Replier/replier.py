import random


class Replier:
    TRIGGER_WORDS = []

    def __init__(self, message):
        self.message = message

    def run(self):
        p = 5 if any(t in self.message.content for t in self.TRIGGER_WORDS) else 10
        r = random.randint(1, p)
        print(r)
        if r == 1:
            return f"Your face is {self.message}"
        if r == 2:
            return "Dint knew."
