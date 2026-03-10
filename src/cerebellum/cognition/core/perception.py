# core/perception.py

from abc import ABC, abstractmethod

from ..core.models import PerceptionResult


class Perception(ABC):

    @abstractmethod
    async def perceive(self, raw_input: str) -> PerceptionResult:
        """
        Convert raw input into structured cognitive representation.
        """
        pass