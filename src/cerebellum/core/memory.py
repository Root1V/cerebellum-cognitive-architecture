# core/memory.py

# Responsabilidad: almacenar y recuperar conocimiento.
# Debe soportar múltiples tipos:
# working memory
# episodic memory
# semantic memory
# procedural memory

from abc import ABC, abstractmethod


class Memory(ABC):

    @abstractmethod
    async def store(self, key, value):
        pass

    @abstractmethod
    async def retrieve(self, query):
        pass

    @abstractmethod
    async def update(self, item):
        pass