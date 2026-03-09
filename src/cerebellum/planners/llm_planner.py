# planners/llm_planner.py

from pydantic import BaseModel

from ..core.planner import Planner
from ..core.llm import LLMClient


class LLMPlanner(Planner):
    """
    LLM-based planner. Falls back to a default plan when no client is provided.

    El llm_client debe implementar el contrato LLMClient (core/llm.py):
        async think(prompt, context, output_model) -> str | BaseModel

    output_model (opcional): clase Pydantic que define la estructura del plan.
    Si se pasa, el planner retorna una instancia validada en lugar de texto crudo.

    Ejemplo:
        from cerebellum.llm import LLMClient
        planner = LLMPlanner(llm_client=LLMClient(model="Mixtral-7B..."), output_model=MyPlan)
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        output_model: type[BaseModel] | None = None,
    ):
        self.llm = llm_client
        self.output_model = output_model

    async def create_plan(self, goal, context=None):
        if self.llm is not None:
            return await self.llm.think(
                prompt=f"Break this goal into ordered steps: {goal}",
                context="You are a planning assistant. Break goals into clear ordered steps.",
                output_model=self.output_model,
            )

        # Default plan when no LLM client is configured
        return [
            {"step": 1, "action": "search_market_data", "goal": goal},
            {"step": 2, "action": "analyze_trends",     "goal": goal},
            {"step": 3, "action": "generate_summary",   "goal": goal},
        ]
