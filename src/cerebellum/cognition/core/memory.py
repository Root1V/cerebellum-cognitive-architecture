# core/memory.py

# Responsabilidad: almacenar y recuperar conocimiento.
# Debe soportar múltiples tipos:
# working memory
# episodic memory
# semantic memory
# procedural memory

from abc import ABC, abstractmethod
from typing import Any


class Memory(ABC):

    @abstractmethod
    async def store(self, key: str, value: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def retrieve(self, query: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update(self, item: Any) -> None:
        raise NotImplementedError