# reasoning/hrm_reasoner.py
from ..core.reasoning import Reasoner
from ..core.planner import Planner
from ..core.memory import Memory
from ..core.tool import Tool

class HierarchicalReasoner(Reasoner):

    def __init__(self, planner: Planner, worker):
        self.planner = planner
        self.worker = worker
    
    async def execute(self, goal, memory: Memory, tools: list[Tool]):

        plan = await self.planner.create_plan(goal)
        results = []

        for step in plan:

            result = await self.worker.solve(
                step,
                memory,
                tools
            )

            results.append(result)

        return results
    
    