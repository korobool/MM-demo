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
        all_nps = None
        all_vps = None
        all_ners = None
        all_tokens = None

    def preprocess(self, raw_text):
        doc = nlp(raw_text)
        self.all_tokens = [token.text for token in doc]
        self.all_nps = [(e.start, e.end) for e in doc.noun_chunks]
        self.all_ners = [(e.start, e.end) for e in doc.ents]
