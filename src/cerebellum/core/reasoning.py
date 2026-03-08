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

from .planner import Planner
from .memory import Memory
from .tool import Tool

class Reasoner(ABC):

    @abstractmethod
    async def execute(self, plan: Planner, memory: Memory, tools: list[Tool]):

        pass
    
    @abstractmethod
    async def reason(self, context):

        """
        Perform reasoning over context
        """

        pass