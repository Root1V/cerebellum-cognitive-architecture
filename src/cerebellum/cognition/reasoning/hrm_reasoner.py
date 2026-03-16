# reasoning/hrm_reasoner.py
from ..core.reasoning import Reasoner
from ..core.planner import Planner
from ..core.memory import Memory
from ...tools.tool import Tool
from ..planners import Plan


class HierarchicalReasoner(Reasoner):

    def __init__(self, planner: Planner, worker):
        self.planner = planner
        self.worker = worker

    async def execute(
        self,
        goal,
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
        # Retrieve past episodes from memory to give the planner context
        context = None
        if "episodic" in memory:
            context = await memory["episodic"].retrieve(str(goal))

        plan: Plan = await self.planner.create_plan(goal, context)
        results = []

        for step in plan.steps:
            result = await self.worker.solve(
                step,
                memory,
                tools
            )
            results.append(result)

        return results
    
    