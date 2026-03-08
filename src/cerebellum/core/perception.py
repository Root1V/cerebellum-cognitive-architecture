# core/perception.py

from abc import ABC, abstractmethod


class Perception(ABC):

    @abstractmethod
    async def perceive(self, input_data: str) -> dict:
        """
        Convert raw input into structured cognitive representation.
        """
        pass