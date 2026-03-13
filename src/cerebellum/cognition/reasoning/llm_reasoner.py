# reasoning/llm_reasoner.py

from ..core.reasoning import Reasoner
from ..core.memory import Memory
from ...tools.tool import Tool
from ...infraestructure.llm.llm import LLM
from ..planners import Plan, PlanStep


class LLMReasoner(Reasoner):
    """
    Reasoner basado en LLM. Consume un Plan estructurado del Planner.

    El llm_client debe implementar el contrato LLMClient (core/llm.py):
        async think(prompt, context, output_model) -> str | BaseModel

    Ejemplo:
        from cerebellum.llm import LLMClient
        reasoner = LLMReasoner(llm_client=LLMClient(model="Mixtral-7B..."))
    """

    def __init__(self, llm_client: LLM | None = None):
        self.llm = llm_client

    async def execute(
        self,
        plan: Plan,
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
        results = []
        for step in plan.steps:
            result = await self.solve(step, memory, tools)
            results.append(result)
        return results

    async def solve(self, step: PlanStep, memory: dict[str, Memory], tools: dict[str, Tool]):
        """
        Ejecuta un paso del plan delegando al recurso adecuado.

        Orden de delegación:
          1. Tool registrada cuyo nombre coincide con el paso.
          2. LLM, si está configurado.
          3. Placeholder genérico (útil en tests / sin infraestructura real).
        """
        action = step.action

        # 1. Delegar a tool registrada por nombre de paso
        tool = tools.get(action) if isinstance(tools, dict) else None
        if tool:
            return await tool.execute()

        # 2. Delegar al LLM
        if self.llm:
            return await self.llm.think(
                prompt=f"Execute step '{action}'. Goal: {step.goal}",
                context="You are a reasoning assistant. Execute the requested step and return the result.",
            )

        # 3. Placeholder — sin tool ni LLM
        return f"executed: {action}"