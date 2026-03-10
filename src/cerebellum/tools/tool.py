# core/tool.py

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):

    name: str

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        pass