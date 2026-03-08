# runtime/cognitive_system.py

class CognitiveSystem:

    def __init__(
        self,
        perception,
        controller,
        memory,
        planner,
        reasoner,
        tools
    ):
        self.perception = perception
        self.controller = controller
        self.memory = memory
        self.planner = planner
        self.reasoner = reasoner
        self.tools = tools

    async def run(self, input_data):

        perception_result = await self.perception.process(input_data)

        goal = await self.controller.interpret(perception_result)

        plan = await self.planner.create_plan(goal)

        result = await self.reasoner.execute(plan, self.memory, self.tools)

        return result