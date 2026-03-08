from ..core.planner import Planner
from ..core.tool import Tool


class SimplePlanner(Planner):
    """
    Planner simple: genera un plan donde cada paso es una tool registrada.

    Al usar los nombres de las tools como nombres de paso, el Planner y el
    Reasoner se acoplan por contrato (step name = tool name), no por strings
    hardcodeados de domínio. Cambiar las tools disponibles cambia el plan
    automáticamente — sin tocar el reasoner.

    Si no hay tools registradas genera un paso genérico 'process' que el
    reasoner delegará al LLM o al placeholder.
    """

    def __init__(self, tools: dict[str, Tool] | None = None):
        self.tools: dict[str, Tool] = tools or {}

    async def create_plan(self, goal: dict, context: list | None = None) -> list[dict]:
        if self.tools:
            return [
                {"step": i + 1, "action": name, "goal": goal}
                for i, name in enumerate(self.tools)
            ]

        # Sin tools: un único paso genérico que el reasoner puede delegar al LLM
        return [{"step": 1, "action": "process", "goal": goal}]
