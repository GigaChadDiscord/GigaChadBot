import random


class Replier:
    TRIGGER_WORDS = []

    def __init__(self):
        self.probability_of_triggered_reply = 10
        self.probability_of_normal_reply = 20
        self.probability_of_question_reply = 4

    def parse(self, message):
        if message.content:
            if message.content[-1] == '?':
                r = random.randint(1, self.probability_of_question_reply)
                if r == 1:
                    return "Perhaps"
            else:
                p = self.probability_of_triggered_reply if any(t in message.content.lower() for t in self.TRIGGER_WORDS) else self.probability_of_normal_reply
                r = random.randint(1, p)
                print(r)
                if r == 1:
                    return f"Your face is {message.content}"
                if r == 2:
                    return "Dint knew"
                if r == 3:
                    return "Really?"
