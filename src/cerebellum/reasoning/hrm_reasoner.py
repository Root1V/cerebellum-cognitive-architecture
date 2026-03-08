# reasoning/hrm_reasoner.py
from ..core.planner import Planner

class HierarchicalReasoner:

    def __init__(self, planner: Planner, worker):
        self.planner = planner
        self.worker = worker

    async def execute(self, goal):

        plan = await self.planner.create_plan(goal)

        results = []

        for step in plan:

            result = await self.worker.solve(step)

            results.append(result)

        return results
    
    