from ..core.controller import CognitiveController
from ..core.perception import Perception


class SimpleController(CognitiveController):
    """
    Controller simple: interpreta la percepción en un goal,
    evalúa si fue satisfecho y no genera subgoals adicionales.
    """

    async def interpret(self, perception: Perception) -> dict:
        """
        Extrae el goal desde la percepción.
        El planner se encargará de dividirlo en pasos concretos.
        """
        return {
            "goal": perception.get("content", ""),
            "intent": perception.get("intent", "analyze"),
            "context": perception.get("context", {}),
        }

    async def is_goal_satisfied(self, goal: dict, result) -> bool:
        """
        Criterio simple: si hay un resultado no vacío, el goal se cumplió.
        En una implementación real, un LLM evaluaría la calidad del resultado.
        """
        return result is not None and result != [] and result != ""

    async def next_goal(self, goal: dict, result) -> dict | None:
        """
        Sin subgoals derivados en la versión simple.
        Retorna None para indicar que el ciclo cognitivo debe detenerse.
        """
        return None

