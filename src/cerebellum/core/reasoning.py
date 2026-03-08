# core/reasoning.py

# Responsabilidad: pensar.
# Aquí vive el:
# LLM
# LRM
# HRM
# RLM

# Ejemplo de implementaciones
# LLMReasoner
# TreeOfThoughtReasoner
# RecursiveReasoner
# HierarchicalReasoner

from abc import ABC, abstractmethod
from typing import Any

from .memory import Memory
from .tool import Tool


class Reasoner(ABC):

    @abstractmethod
    async def execute(
        self,
        plan: list[dict],
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
        """
        Execute reasoning over a structured plan.

        Parameters
        ----------
        plan   : list of step dicts produced by the Planner.
        memory : memory system dict keyed by memory type.
        tools  : available tools keyed by name.
        """
        ...

    @abstractmethod
    async def reason(self, context: dict) -> Any:
        """
        Perform reasoning over context.
        """
        ...