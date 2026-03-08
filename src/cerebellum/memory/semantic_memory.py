# maybe vector database
# maybe knowledge graph

class SemanticMemory:
    def __init__(self):
        self.knowledge = {}

    def store(self, key, value):
        self.knowledge[key] = value

    def retrieve(self, key):
        return self.knowledge.get(key)