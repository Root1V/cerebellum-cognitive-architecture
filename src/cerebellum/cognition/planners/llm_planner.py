# planners/llm_planner.py

from ..core.planner import Planner
from ..core.models import Plan, PlanStep
from ...infraestructure.llm.llm import LLMClient


class LLMPlanner(Planner):
    """
    LLM-based planner. Siempre retorna un Plan estructurado.

    El llm_client debe implementar el contrato LLMClient (core/llm.py):
        async think(prompt, context, output_model) -> str | BaseModel

    Ejemplo:
        from cerebellum.llm import LLMClient
        planner = LLMPlanner(llm_client=LLMClient(model="Mixtral-7B..."))
        plan = await planner.create_plan(goal="Analizar mercado IA en LATAM")
        # plan es siempre una instancia de Plan
    """

    def __init__(self, llm_client: LLMClient | None = None):
        self.llm = llm_client

    async def create_plan(self, goal, context=None) -> Plan:
        if self.llm is not None:
            return await self.llm.think(
                prompt=f"Break this goal into ordered steps: {goal}",
                context="You are a planning assistant. Break goals into clear ordered steps.",
                output_model=Plan,
            )

        # Default plan cuando no hay LLM configurado
        return Plan(steps=[
            PlanStep(step=1, action="search_market_data", goal=str(goal)),
            PlanStep(step=2, action="analyze_trends",     goal=str(goal)),
            PlanStep(step=3, action="generate_summary",   goal=str(goal)),
        ])

