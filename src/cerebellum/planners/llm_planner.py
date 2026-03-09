# planners/llm_planner.py

from ..core.planner import Planner
from ..core.llm import LLMClient


class LLMPlanner(Planner):
    """
    LLM-based planner. Falls back to a default plan when no client is provided.

    El llm_client debe implementar el contrato LLMClient (core/llm.py):
        async think(prompt, context) -> str

    Ejemplo:
        from cerebellum.llm import LLMClient
        planner = LLMPlanner(llm_client=LLMClient(model="Mixtral-7B..."))
    """

    def __init__(self, llm_client: LLMClient | None = None):
        self.llm = llm_client

    async def create_plan(self, goal, context=None):
        if self.llm is not None:
            return await self.llm.think(
                prompt=f"Break this goal into ordered steps: {goal}",
                context="You are a planning assistant. Break goals into clear ordered steps.",
            )

        # Default plan when no LLM client is configured
        return [
            {"step": 1, "action": "search_market_data", "goal": goal},
            {"step": 2, "action": "analyze_trends",     "goal": goal},
            {"step": 3, "action": "generate_summary",   "goal": goal},
        ]
