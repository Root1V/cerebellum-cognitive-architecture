# reasoning/llm_reasoner.py

from ..core.reasoning import Reasoner
from ..core.planner import Planner
from ..core.memory import Memory
from ..core.tool import Tool

class LLMReasoner(Reasoner):

    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def solve(self, step, memory: Memory, tools: list[Tool]):

        if step["step"] == "search_market_data":

            tool: Tool = tools["web_search"]

            return await tool.execute(
                query="AI market Latin America"
            )

        if step["step"] == "analyze_trends":

            return await self.llm.complete(
                f"AI adoption growing in fintech and healthcare: {step}"
            )

        if step["step"] == "generate_summary":

            return "AI market in LATAM shows strong growth potential"

        return "unknown step"