# core/controller.py

from abc import ABC, abstractmethod

from .perception import Perception


class CognitiveController(ABC):

    @abstractmethod
    async def interpret(self, perception: Perception):
        pass
    