import torch
import copy
import math
import copy
import spacy
import collections

from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM

nlp = spacy.load('en')


class EntityNodesFinder:
    def __init__(self):
        self.all_nps = []
        # self.all_vps = []
        self.all_ners = []
        self.all_tokens = []

    def preprocess(self, raw_text):
        doc = nlp(raw_text)
        self.all_tokens = [token.text for token in doc]
        self.all_nps = [(e.start, e.end-1) for e in doc.noun_chunks]
        self.all_ners = [(e.start, e.end-1) for e in doc.ents]


class NodesBertScoring:
    def __init__(self, factorize=True):
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.weight_of_phrase = []
        self.weight_of_position = []
        self.weight_average = []
        self.factorize = factorize

    def to_low(self, inp_list):
        return [x.lower() for x in inp_list]

    def merge(self, inp_list, bert_list):
        dif = list(set(inp_list).difference(bert_list))
        for x in dif:
            for n, y in enumerate(inp_list):
                if x == y:
                    inp_list[n] = '[UNK]'
        return inp_list

    def _bert_weight_of_phrase(self, tokenized_text, ner_list):
        results = []
        for n in ner_list:
            weight_factor_sum = 0
            for i in range(n[0], n[1] + 1):
                weight_factor = 100
                tokenized_text_copy = copy.copy(tokenized_text)
                tokenized_text_copy[i] = '[MASK]'
                # print(tokenized_text_copy)
                # print(tokenized_text_copy)
                # Convert token to vocabulary indices
                indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text_copy)

                # Define sentence A and B indices associated to 1st and 2nd sentences (see paper)
                segments_ids = [0] * len(tokenized_text_copy)

                # Convert inputs to PyTorch tensors
                tokens_tensor = torch.tensor([indexed_tokens])
                segments_tensors = torch.tensor([segments_ids])

                # Predict all tokens
                predictions = self.model(tokens_tensor, segments_tensors)

                item, pred = torch.sort(predictions[0, i], descending=True)
                predicted_tokens = []
                for index in pred[:100]:
                    predicted_tokens.append(self.tokenizer.convert_ids_to_tokens([index.item()])[0])
                for one_token in predicted_tokens:
                    if one_token != tokenized_text[i]:
                        weight_factor -= 1
                    else:
                        break
                weight_factor_sum += weight_factor / 100
            weight_factor_sum /= (n[1] - n[0] + 1)
            results.append([' '.join(tokenized_text[n[0]: n[1] + 1]), weight_factor_sum])
        return results

    def _bert_weight_of_position(self, tokenized_text, ner_list):
        results = []
        for n in ner_list:
            weight_factor_sum = 0
            actual_range = [n[0], n[1]]
            if n[0] != 0:
                actual_range.insert(0, n[0] - 1)
            if n[1] != len(ner_list):
                actual_range.append(n[0] + 1)
            for i in actual_range:
                weight_factor = 100
                tokenized_text_copy = copy.copy(tokenized_text)
                tokenized_text_copy[i] = '[MASK]'
                # print(tokenized_text_copy)
                # print(tokenized_text_copy)
                # Convert token to vocabulary indices
                indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text_copy)

                # Define sentence A and B indices associated to 1st and 2nd sentences (see paper)
                segments_ids = [0] * len(tokenized_text_copy)

                # Convert inputs to PyTorch tensors
                tokens_tensor = torch.tensor([indexed_tokens])
                segments_tensors = torch.tensor([segments_ids])

                # Predict all tokens
                predictions = self.model(tokens_tensor, segments_tensors)

                item, pred = torch.sort(predictions[0, i], descending=True)
                predicted_tokens = []
                for index in pred[:100]:
                    predicted_tokens.append(self.tokenizer.convert_ids_to_tokens([index.item()])[0])
                for one_token in predicted_tokens:
                    if one_token != tokenized_text[i]:
                        weight_factor -= 1
                    else:
                        break
                weight_factor_sum += weight_factor / 100
            weight_factor_sum /= len(actual_range)
            results.append([' '.join(tokenized_text[n[0]: n[1] + 1]), weight_factor_sum])
        return results

    def factorizer(self, data):
        result = []
        for x in data:
            result.append([x[0], round((math.pow(101, x[1]) - 1), 1)])
        return result

    def un_unk(self):
        index = 0
        for data in [self.weight_of_phrase, self.weight_of_position, self.weight_average]:
            result = []
            for x in data:
                if x[0] != '[UNK]':
                    result.append(x)
            if index == 0:
                self.weight_of_phrase = result
                index += 1
            if index == 1:
                self.weight_of_position = result
                index += 1
            if index == 2:
                self.weight_average = result

    def take_second(self, elem):
        return elem[1]

    def repeat_killer(self, data):
        a = [x[0] for x in data]
        b = [item for item, count in collections.Counter(a).items() if count > 1]
        if not b:
            return data
        result = []
        for item1 in b:
            c = [x for x in data if x[0] == item1]
            c.sort(key=self.take_second, reverse=True)
            result.append(c[0])
        names = [x[0] for x in result]
        for item2 in data:
            if item2[0] not in names:
                result.append(item2)
        return result

    def _average_weighting(self, weight_of_phrase, weight_of_position, k=0.5, m=0.5):
        results = []
        for one_entity_1, one_entity_2 in zip(weight_of_phrase, weight_of_position):
            weight = (one_entity_1[1] * k + one_entity_2[1] * m) / (k + m)
            results.append([one_entity_1[0], weight])
        return results

    def analyze(self, text, tokenized_text_inp, ner_list, nps_list):
        print('ner', ner_list)
        print('nps', nps_list)
        ent_list = list(set(ner_list + nps_list))
        print('ent', ent_list)
        tokenized_text_bert = self.tokenizer.tokenize(text)
        tokenized_text_inp = self.to_low(tokenized_text_inp)
        tokenized_text = self.merge(tokenized_text_inp, tokenized_text_bert)
        self.weight_of_phrase = self._bert_weight_of_phrase(tokenized_text, ent_list)
        self.weight_of_position = self._bert_weight_of_position(tokenized_text, ent_list)
        self.weight_average = self._average_weighting(self.weight_of_phrase, self.weight_of_position)

        self.un_unk()

        if self.factorize:
            self.weight_of_phrase = self.factorizer(self.weight_of_phrase)
            self.weight_of_position = self.factorizer(self.weight_of_position)
            self.weight_average = self.factorizer(self.weight_average)

        self.weight_of_phrase = self.repeat_killer(self.weight_of_phrase)
        self.weight_of_position = self.repeat_killer(self.weight_of_position)
        self.weight_average = self.repeat_killer(self.weight_average)

        print(self.weight_of_phrase)
        print(self.weight_of_position)
        print(self.weight_average)
