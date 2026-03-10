
from abc import ABC, abstractmethod
from typing import List

from ..core.models import CognitiveState, Fact


class RuleEnginePort(ABC):
    @abstractmethod
    def derive(self, facts: List[Fact], state: CognitiveState) -> List[Fact]:
        raise NotImplementedError

