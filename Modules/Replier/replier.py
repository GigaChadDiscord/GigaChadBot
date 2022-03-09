import random


class Replier:
    TRIGGER_WORDS = []

    def __init__(self, message):
        self.message = message

    def run(self):
        if self.message.content[-1] == '?':
            return "Perhaps"
        p = 10 if any(t in self.message.content.lower() for t in self.TRIGGER_WORDS) else 20
        r = random.randint(1, p)
        print(r)
        if r == 1:
            return f"Your face is {self.message.content}"
        if r == 2:
            return "Dint knew"
        if r == 3:
            return "Really?"
