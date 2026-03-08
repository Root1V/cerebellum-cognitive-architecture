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


class Planner(ABC):

    @abstractmethod
    async def create_plan(self, goal, context):
        """
        Decompose goal into tasks
        """
        pass