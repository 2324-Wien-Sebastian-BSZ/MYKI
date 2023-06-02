import re
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

class SimpleChatBot:
    def __init__(self, pairs, reflections):
        self.pairs = pairs
        self.reflections = reflections
        self.vectorizer = CountVectorizer()
        self.classifier = None

    def _reflect(self, phrase):
        tokens = phrase.lower().split()
        tokens = [self.reflections.get(token, token) for token in tokens]
        return ' '.join(tokens)

    def _prepare_data(self, pairs):
        X = []
        y = []
        for pattern, _ in pairs:
            X.append(pattern)
            y.append(pattern)
        return X, y

    def _train_classifier(self, X, y):
        X_vectorized = self.vectorizer.fit_transform(X)
        self.classifier = MultinomialNB()  # Naive Bayes Classifier
        # self.classifier = SVC()  # Support Vector Machines Classifier
        # self.classifier = DecisionTreeClassifier()  # Decision Trees Classifier
        self.classifier.fit(X_vectorized, y)

    def _match_and_respond(self, statement):
        statement_vectorized = self.vectorizer.transform([statement])
        predicted_intent = self.classifier.predict(statement_vectorized)[0]

        for pattern, responses in self.pairs:
            if pattern == predicted_intent:
                response = random.choice(responses)
                if "%1" in response:
                    response = response.replace("%1", self._reflect(statement))
                return response
        return None

    def add_pairs(self, new_pairs):
        self.pairs.extend(new_pairs)

    def train(self):
        X, y = self._prepare_data(self.pairs)
        self._train_classifier(X, y)

    def respond_to(self, statement):
        response = self._match_and_respond(statement)
        if response is None:
            return "I'm sorry, I didn't understand that."
        else:
            return response

# Beispiel-Paarliste und Reflexionswörterbuch
pairs = [
    (r'I need (.+)', [
        "Why do you need %1?",
        "Would it really help you to get %1?",
        "Are you sure you need %1?"]),
    (r'Why don\'t you (.+)', [
        "Do you really think I don't %1?",
        "Perhaps eventually I will %1.",
        "Do you really want me to %1?"]),
]

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'm": "you are",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "you are": "I am",
    "you were": "I was",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

chatbot = SimpleChatBot(pairs, reflections)

# Neue Paare hinzufügen
new_pairs = [
    (r'Hello', [
        "Hi there!",
        "Hello, how can I help you?"]),
    (r'What is your name\?', [
        "My name is ChatBot.",
        "I'm ChatBot, nice to meet you."]),
]

chatbot.add_pairs(new_pairs)
chatbot.train()

inputstr = ""
while inputstr != "quit":
    inputstr = input("> ")
    print(chatbot.respond_to(inputstr))
