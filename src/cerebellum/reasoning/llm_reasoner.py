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
        # Support both plan formats:
        #   new: {"action": "search_market_data", ...}
        #   legacy: {"step": "search_market_data", ...}
        action = step.get("action") or step.get("step")

        if action == "search_market_data":
            tool = tools.get("web_search")
            if tool:
                return await tool.execute(query="AI market Latin America")
            return "Search results for AI market Latin America"

        if action == "analyze_trends":
            if self.llm:
                return await self.llm.complete(
                    f"AI adoption growing in fintech and healthcare: {step}"
                )
            return "AI adoption growing in fintech and healthcare"

        if action == "generate_summary":
            return "AI market in LATAM shows strong growth potential"

        return f"unknown action: {action}"