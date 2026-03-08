# core/controller.py

from abc import ABC, abstractmethod


class CognitiveController(ABC):
    """
    Executive controller — decide qué quiere lograr el agente.

    Responsabilidades
    -----------------
    interpret()          → traduce la percepción en un goal estructurado
    is_goal_satisfied()  → evalúa si el resultado cumple el objetivo
    next_goal()          → devuelve un subgoal derivado, o None si ya terminó
    """

    @abstractmethod
    async def interpret(self, focused: dict) -> dict:
        """Traduce la percepción filtrada en un goal estructurado."""
        pass

    @abstractmethod
    async def is_goal_satisfied(self, goal: dict, result) -> bool:
        """Retorna True cuando el resultado cumple el objetivo."""
        pass

    @abstractmethod
    async def next_goal(self, goal: dict, result) -> dict | None:
        """
        Devuelve un subgoal derivado si el trabajo no terminó,
        o None si el objetivo principal ya fue alcanzado.
        """
        pass
