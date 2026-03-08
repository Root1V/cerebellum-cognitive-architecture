from ..core.planner import Planner

class SimplePlanner(Planner):

    async def create_plan(self, goal, context=None):

        return [
            {"step": "analyze", "goal": goal},
            {"step": "reason", "goal": goal}
        ]
        