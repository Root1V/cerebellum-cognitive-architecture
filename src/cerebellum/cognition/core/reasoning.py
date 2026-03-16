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
from .models import Plan
from ...tools.tool import Tool


class Reasoner(ABC):

    @abstractmethod
    async def execute(
        self,
        plan: Plan,
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> Any:
        """
        Execute reasoning over a structured plan.

        Parameters
        ----------
        plan   : The plan produced by the Planner.
        memory : memory system dict keyed by memory type.
        tools  : available tools keyed by name.
        """
        ...