import json
import pandas
import numpy as np
from gensim import models


class MMGraphAnalyzer:
    def __init__(self):
        self.model = models.Doc2Vec.load('../d2w_model/model.bin')
        self.matrix_shape = 10
        self.n = 5
        self.tree = {}

    def compare_sentences(self, sentence_a, sentence_b, iters=50):
        s = 0
        if sentence_a == sentence_b:
            return 1.0
        for i in range(iters):
            a = self.model.infer_vector(sentence_a.split(), steps=10)
            b = self.model.infer_vector(sentence_b.split(), steps=10)
            s += np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)
        return s / iters

    def take_second(self, elem):
        return elem[1]

    def check_max_repeat(self, ent):
        first_max = ent[0]
        result = []
        for x in ent:
            if x[1] == first_max[1]:
                result.append(x)
        return result

    def check_max_score(self, ent_max, matrix):
        result = [0] * len(ent_max)
        for number in range(len(ent_max)):
            sum_row = 0
            sum_col = 0
            for i in range(self.matrix_shape):
                sum_row += matrix[number, i]
                sum_col += matrix[i, number]
            sum_row -= 1
            sum_col -= 1
            result[number] = sum_row + sum_col
        return result.index(max(result))

    def find_n_nodes(self, parent_node_num, matrix, labels):
        nodes = []
        for i in range(self.matrix_shape):
            i_row = matrix[parent_node_num, i]
            if (i_row != 0) and (i_row != 1):
                nodes.append([labels[i], i_row])
            i_col = matrix[i, parent_node_num]
            if (i_col != 0) and (i_col != 1):
                nodes.append([labels[i], i_col])
        nodes.sort(key=self.take_second, reverse=True)
        result = [x[0] for x in nodes[:self.n]]
        return result

    def find_rest_nodes(self, second_level_nodes, matrix, labels, parent_node):
        result = []
        for node in labels:
            if (node not in second_level_nodes) and node != parent_node:
                nodes_list = []
                node_num = labels.index(node)
                for i in range(self.matrix_shape):
                    i_row = matrix[node_num, i]
                    if (i_row != 0) and (i_row != 1) and (labels[i] in second_level_nodes):
                        nodes_list.append([labels[i], i_row])
                    i_col = matrix[i, node_num]
                    if (i_col != 0) and (i_col != 1) and (labels[i] in second_level_nodes):
                        nodes_list.append([labels[i], i_col])
                nodes_list.sort(key=self.take_second, reverse=True)
                result.append([nodes_list[0][0], node])
        return result

    def analyze(self, entities):
        entities.sort(key=self.take_second, reverse=True)
        entities_popular = entities[:self.matrix_shape]
        relationship_matrix = np.zeros(shape=(self.matrix_shape, self.matrix_shape), dtype=float)

        for i in range(self.matrix_shape):
            for j in range(i, self.matrix_shape):
                relationship_matrix[i, j] = self.compare_sentences(entities_popular[i][0], entities_popular[j][0])

        labels = [x[0] for x in entities_popular]
        entities_popular_max = self.check_max_repeat(entities_popular)
        parent_node_num = self.check_max_score(entities_popular_max, relationship_matrix)
        self.tree = {'text': labels[parent_node_num], 'id': 0, 'nodes': []}
        second_level_nodes = self.find_n_nodes(parent_node_num, relationship_matrix, labels)

        for i in range(len(second_level_nodes)):
            self.tree['nodes'].append({'text': second_level_nodes[i], 'id': i + 1, 'nodes': []})

        third_level_nodes = self.find_rest_nodes(second_level_nodes,
                                                 relationship_matrix,
                                                 labels,
                                                 labels[parent_node_num])
        idx = len(second_level_nodes) + 1
        for node in third_level_nodes:
            for x in self.tree['nodes']:
                if x['text'] == node[0]:
                    x['nodes'].append({'text': node[1], 'id': idx, 'nodes': []})
                    idx += 1
