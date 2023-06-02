import re
import random

class SimpleChatBot:
    def __init__(self, pairs, reflections):
        self.pairs = pairs
        self.reflections = reflections

    def _reflect(self, phrase):
        tokens = phrase.lower().split()
        for i, token in enumerate(tokens):
            if token in self.reflections:
                tokens[i] = self.reflections[token]
        return ' '.join(tokens)

    def _match_and_respond(self, statement):
        for pattern, responses in self.pairs:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.replace("%1", self._reflect(match.group(1)))
        return None

    def respond_to(self, statement):
        response = self._match_and_respond(statement)
        if response is None:
            return "I'm sorry, I didn't understand that."
        else:
            return response

# Beispiel-Paarliste und Reflexionswörterbuch
pairs = [
    (r'I need (.*)',
    ["Why do you need %1?",
     "Would it really help you to get %1?",
     "Are you sure you need %1?"]),

    (r'Why don\'t you (.*)',
    ["Do you really think I don't %1?",
     "Perhaps eventually I will %1.",
     "Do you really want me to %1?"]),
]

reflections = {
    "am"   : "are",
    "was"  : "were",
    "i"    : "you",
    "i'm"  : "you are",
    "i'd"  : "you would",
    "i've"  : "you have",
    "i'll"  : "you will",
    "my"  : "your",
    "you are"  : "I am",
    "you were" : "I was",
    "you've" : "I have",
    "you'll" : "I will",
    "your"  : "my",
    "yours" : "mine",
    "you"   : "me",
    "me"  : "you"
}

chatbot = SimpleChatBot(pairs, reflections)
inputstr = ""
while inputstr != "quit":
    inputstr=hiinput("> ")
    print(chatbot.respond_to(inputstr))
