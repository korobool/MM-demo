import random


class WeightedListAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text):
        result = []
        text_list = text.split()
        for item in text_list:
            result.append((item, random.randint(1, 101)))
        return result
