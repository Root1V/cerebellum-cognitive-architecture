# core/planner.py

# Convierte objetivos en secuencias de acciones.
# Ejemplo:
# Goal:
# create financial report
# Plan:
# 1 collect data
# 2 analyze trends
# 3 generate charts
# 4 write report

from abc import ABC, abstractmethod

from cerebellum.cognition.core.models import Plan


class Planner(ABC):

    @abstractmethod
    async def create_plan(self, goal: dict, context: list | None = None) -> Plan:
        """
        Decompose goal into tasks.
        """
        pass