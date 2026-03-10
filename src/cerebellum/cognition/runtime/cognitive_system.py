# runtime/cognitive_system.py

from ..core.action import Action
from ..core.attention import Attention
from ..core.controller import CognitiveController
from ..core.environment import Environment
from ..core.learning import Experience, Learning
from ..core.memory import Memory
from ..core.perception import Perception
from ..core.planner import Planner
from ..core.reasoning import Reasoner
from ...tools.tool import Tool
from ...infraestructure.observability.tracer import Tracer
from ...infraestructure.observability.metrics import Metrics
from typing import Any

_MAX_GOAL_DEPTH = 5


class CognitiveSystem:

    def __init__(
        self,
        perception: Perception,
        attention: Attention,
        memory: dict[str, Memory],
        planner: Planner,
        reasoner: Reasoner,
        action: Action,
        learning: Learning,
        environment: Environment,
        controller: CognitiveController,
        tools: dict[str, Tool] | None = None,
        tracer: Tracer | None = None,
        metrics: Metrics | None = None
    ):

        self.perception: Perception = perception
        self.attention: Attention = attention
        self.memory: dict[str, Memory] = memory
        self.planner: Planner = planner
        self.reasoner: Reasoner = reasoner
        self.action: Action = action
        self.learning: Learning = learning
        self.environment: Environment = environment
        self.controller: CognitiveController = controller
        self.tools: dict[str, Tool] = tools or {}
        self.metrics: Metrics | None = metrics
        self.tracer: Tracer | None = tracer

    async def run(self, input_data: str, _depth: int = 0) -> Any:

        if self.tracer:
            self.tracer.trace("input_received", input_data)

        # 0. Environment observation — world state enriches the cognitive cycle
        env_state = self.environment.observe()

        # 1. Perception
        perception = await self.perception.perceive(input_data)
        # Merge environment state so attention has access to the full world context
        perception["env"] = env_state

        # 2. Attention — filter what is relevant from perception + memory
        focused = await self.attention.select(perception, self.memory)

        # 3. Controller interprets focused input into a goal
        goal = await self.controller.interpret(focused)

        # 4. Memory retrieval — past experiences to enrich planning
        context = await self.memory["episodic"].recall(goal["goal"])

        # 5. Planning
        plan = await self.planner.create_plan(goal, context)

        # 6. Reasoning
        error = None
        try:
            result = await self.reasoner.execute(
                plan,
                self.memory,
                self.tools
            )
        except Exception as exc:
            error = exc
            result = None

        # 6.5. Action — translate reasoning output into an environmental effect
        # This is where the agent actually does something in the world.
        action_result = None
        if result is not None and error is None:
            try:
                action_result = await self.action.execute(result)
                self.environment.update(action_result)
                if self.tracer:
                    self.tracer.trace("action_executed", action_result)
            except Exception as exc:
                error = exc

        # 7. Learning — record the experience with the action outcome
        experience = Experience(
            result=action_result if action_result is not None else result,
            error=error,
            feedback=None,
            success=error is None and result is not None,
            context={"goal": goal, "plan": plan},
        )
        await self.learning.update(experience)

        # 7.5. Metrics — track outcome of this cognitive cycle
        if self.metrics:
            self.metrics.increment("runs")
            if experience.success:
                self.metrics.increment("successes")
            else:
                self.metrics.increment("errors")

        # 8. Store episodic memory
        await self.memory["episodic"].store_event({
            "goal": goal,
            "result": result
        })

        # 9. Controller evaluates whether the goal was satisfied
        satisfied = await self.controller.is_goal_satisfied(goal, result)
        if not satisfied:
            if _depth >= _MAX_GOAL_DEPTH:
                # Prevent infinite recursion when goal is never satisfied
                if error:
                    raise error
                return result
            next_goal = await self.controller.next_goal(goal, result)
            if next_goal:
                return await self.run(next_goal["goal"], _depth + 1)

        if error:
            raise error

        return action_result if action_result is not None else result