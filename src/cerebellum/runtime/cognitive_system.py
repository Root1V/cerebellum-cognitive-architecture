# runtime/cognitive_system.py

# runtime/cognitive_system.py
    
class CognitiveSystem:

    def __init__(
        self,
        perception,
        attention,
        memory,
        planner,
        reasoner,
        action,
        learning,
        environment,
        controller=None,
        tools=None,
        tracer=None,
        metrics=None
    ):

        self.perception = perception
        self.attention = attention
        self.memory = memory
        self.planner = planner
        self.reasoner = reasoner
        self.action = action
        self.learning = learning
        self.environment = environment
        self.controller = controller
        self.tools = tools or []
        self.metrics = metrics
        self.tracer = tracer

        self.goal = None
        self.result = None

    def set_goal(self, goal):
        self.goal = goal
        
    def step(self):
        # 1 perception
        raw_input = self.environment.observe()

        perception_output = self.perception.perceive(raw_input)

        # 2 attention
        focused = self.attention.filter(perception_output)

        # 3 memory retrieval
        context = self.memory.retrieve("context")

        # 4 planning
        plan = self.planner.plan(self.goal, focused, context)

        # 5 reasoning
        reasoning_output = self.reasoner.reason(plan)

        # 6 action
        action_result = self.action.execute(reasoning_output)

        # 7 environment update
        self.environment.update(action_result)

        # 8 learning
        self.learning.update(self.memory, action_result)

        self.result = action_result

    def is_finished(self):
        return self.result is not None
    
    async def run(self, input_data):

        if self.tracer:
            self.tracer.trace("input_received", input_data)

        # Perception
        perception = await self.perception.perceive(input_data)

        # Controller interprets goal (optional)
        if self.controller:
            goal = await self.controller.interpret(perception)
        else:
            goal = {"goal": perception.get("content", input_data)}

        # Retrieve memory
        context = await self.memory["episodic"].recall(goal["goal"])

        # Planning
        plan = await self.planner.create_plan(goal)

        # Reasoning
        result = await self.reasoner.execute(
            plan,
            self.memory,
            self.tools or []
        )

        # Store memory
        await self.memory["episodic"].store_event({
            "goal": goal,
            "result": result
        })

        return result