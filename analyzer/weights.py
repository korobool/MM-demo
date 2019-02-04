import random
import spacy

nlp = spacy.load('en')


class NodesBertScoring:
    def __init__(self):
        pass

    def analyze(self, text):
        result = []
        text_list = text.split()
        for item in text_list:
            result.append((item, random.randint(1, 101)))
        return result


class EntityNodesFinder:
    def __init__(self):
        self.all_nps = []
        self.all_vps = []
        self.all_ners = []
        self.all_tokens = []

    def preprocess(self, raw_text):
        doc = nlp(raw_text)
        self.all_tokens = [token.text for token in doc]
        self.all_nps = [(e.start, e.end-1) for e in doc.noun_chunks]
        self.all_ners = [(e.start, e.end-1) for e in doc.ents]
