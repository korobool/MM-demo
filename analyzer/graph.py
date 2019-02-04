class MMGraphAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text, weights):
        result = {"id": 0,
                  "nodes": [{"id": 10, "nodes": [], "text": "test_node1"},
                            {"id": 20, "nodes": [{"id": 70, "nodes": [], "text": "test_node7"}]}],
                  "text": "root"}
        return result