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

from .memory import Memory
from .tool import Tool


class Reasoner(ABC):

    @abstractmethod
    async def execute(self, plan: list[dict], memory: Memory, tools: dict[str, Tool]):
        """
        Execute reasoning over a structured plan.

        Parameters
        ----------
        plan   : list of step dicts produced by the Planner.
        memory : memory system dict.
        tools  : available tools keyed by name.
        """
        ...

    @abstractmethod
    async def reason(self, context):
        """
        Perform reasoning over context.
        """
        ...