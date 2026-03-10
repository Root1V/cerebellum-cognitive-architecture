from abc import ABC, abstractmethod

from ..core.models import NeuralInterpretation


class NeuralEngine(ABC):
    @abstractmethod
    async def interpret(self, text: str) -> NeuralInterpretation:
        raise NotImplementedError
