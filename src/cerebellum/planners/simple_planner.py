from ..core.planner import Planner


class SimplePlanner(Planner):
    """
    Planner simple basado en reglas.
    Descompone cualquier goal en tres pasos canónicos.
    Las action names están alineadas con lo que el reasoner puede ejecutar.
    """

    async def create_plan(self, goal, context=None) -> list[dict]:
        return [
            {"step": 1, "action": "search_market_data", "goal": goal},
            {"step": 2, "action": "analyze_trends",     "goal": goal},
            {"step": 3, "action": "generate_summary",   "goal": goal},
        ]
        