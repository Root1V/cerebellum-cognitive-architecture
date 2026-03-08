# reasoning/llm_reasoner.py

from ..core.reasoning import Reasoner
from ..core.planner import Planner
from ..core.memory import Memory
from ..core.tool import Tool

class LLMReasoner(Reasoner):

    def __init__(self, llm_client):
        self.llm = llm_client

    async def execute(self, plan: Planner, memory: Memory, tools: list[Tool]):

        results = []

        for step in plan:

            response = await self.llm.complete(
                f"Execute step: {step}"
            )

            results.append(response)

        return results