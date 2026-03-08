# core/tool.py

from abc import ABC, abstractmethod


class Tool(ABC):

    name: str

    @abstractmethod
    async def execute(self, **kwargs):
        pass