# planners/llm_planner.py

from pydantic import BaseModel, Field

from ..core.planner import Planner
from ..core.llm import LLMClient


class PlanStep(BaseModel):
    step:   int = Field(description="Execution order of this step, starting at 1.")
    action: str = Field(description="Name of the tool or cognitive action to invoke, e.g. 'search_market_data' or 'analyze_trends'.")
    goal:   str = Field(description="Specific sub-objective this step must accomplish, expressed as a concrete outcome.")


class Plan(BaseModel):
    steps: list[PlanStep] = Field(description="Ordered list of steps that fully decompose the goal. Each step maps to one tool or action.")


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
