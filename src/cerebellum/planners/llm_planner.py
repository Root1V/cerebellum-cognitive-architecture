# planners/llm_planner.py

from ..core.planner import Planner


class LLMPlanner(Planner):
    """
    LLM-based planner. Falls back to a default plan when no client is provided.

    El llm_client debe implementar:
        async complete(prompt: str) -> str

    Compatible con cerebellum.llm.LlamaAdapter (axonium-sdk).

    Ejemplo:
        from cerebellum.llm import LlamaAdapter
        planner = LLMPlanner(llm_client=LlamaAdapter(model="Mixtral-7B..."))
    """

    def __init__(self, llm_client=None):
        self.llm = llm_client

    async def create_plan(self, goal, context=None):
        if self.llm is not None:
            response = await self.llm.complete(
                f"Break this goal into ordered steps: {goal}"
            )
            return response

        # Default plan when no LLM client is configured
        return [
            {"step": 1, "action": "search_market_data", "goal": goal},
            {"step": 2, "action": "analyze_trends",     "goal": goal},
            {"step": 3, "action": "generate_summary",   "goal": goal},
        ]
