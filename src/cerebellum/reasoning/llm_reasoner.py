# reasoning/llm_reasoner.py

from ..core.reasoning import Reasoner
from ..core.memory import Memory
from ..core.tool import Tool


class LLMReasoner(Reasoner):
    """
    Reasoner basado en LLM.

    El llm_client debe implementar:
        async complete(prompt: str) -> str

    Compatible con cerebellum.llm.LlamaAdapter (axonium-sdk).

    Ejemplo:
        from cerebellum.llm import LlamaAdapter
        reasoner = LLMReasoner(llm_client=LlamaAdapter(model="Mixtral-7B..."))
    """

    def __init__(self, llm_client=None):
        self.llm = llm_client

    async def execute(
        self,
        plan: list[dict],
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
        results = []
        for step in plan:
            result = await self.solve(step, memory, tools)
            results.append(result)
        return results

    async def solve(self, step: dict, memory: dict[str, Memory], tools: dict[str, Tool]):
        """
        Ejecuta un paso del plan delegando al recurso adecuado.

        Orden de delegación:
          1. Tool registrada cuyo nombre coincide con el paso.
          2. LLM, si está configurado.
          3. Placeholder genérico (útil en tests / sin infraestructura real).
        """
        action = step.get("action") or step.get("step")

        # 1. Delegar a tool registrada por nombre de paso
        tool = tools.get(action) if isinstance(tools, dict) else None
        if tool:
            return await tool.execute()

        # 2. Delegar al LLM
        if self.llm:
            return await self.llm.complete(
                f"Execute step '{action}'. Context: {step}"
            )

        # 3. Placeholder — sin tool ni LLM
        return f"executed: {action}"