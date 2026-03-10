
from abc import ABC, abstractmethod
from typing import List

from ..core.models import ConstraintViolation, Fact


class RuleEngine(ABC):
    @abstractmethod
    def derive(self, facts: List[Fact]) -> List[Fact]:
        raise NotImplementedError


class ConstraintEngine(ABC):
    @abstractmethod
    def validate(self, facts: List[Fact]) -> List[ConstraintViolation]:
        raise NotImplementedError
