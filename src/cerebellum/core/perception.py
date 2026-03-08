# core/perception.py

from abc import ABC, abstractmethod


class Perception(ABC):

    @abstractmethod
    async def perceive(self, input_data):
        """
        Convert raw input into structured cognitive representation
        """
        pass