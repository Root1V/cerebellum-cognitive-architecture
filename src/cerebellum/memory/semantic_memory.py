# maybe vector database
# maybe knowledge graph

from typing import Any

from ..core.memory import Memory


class SemanticMemory(Memory):
    """
    Memoria semántica: conocimiento del mundo (hechos, documentos, knowledge base).
    """

    def __init__(self):
        self.knowledge: dict[str, Any] = {}

    async def store(self, key, value) -> None:
        self.knowledge[key] = value

    async def retrieve(self, query) -> Any:
        return self.knowledge.get(query)

    async def update(self, item: dict) -> None:
        if isinstance(item, dict):
            self.knowledge.update(item)