from ..core.planner import Planner

class SimplePlanner(Planner):

    async def create_plan(self, goal):

        return [
            {"step": "analyze", "goal": goal},
            {"step": "reason", "goal": goal}
        ]
        