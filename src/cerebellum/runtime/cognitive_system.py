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
from ..core.tool import Tool
from ..observability.tracer import Tracer
from ..observability.metrics import Metrics
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
        controller: CognitiveController | None = None,
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
        self.controller: CognitiveController | None = controller
        self.tools: dict[str, Tool] = tools or {}
        self.metrics: Metrics | None = metrics
        self.tracer: Tracer | None = tracer

    async def run(self, input_data: str, _depth: int = 0) -> Any:

        if self.tracer:
            self.tracer.trace("input_received", input_data)

        # 1. Perception
        perception = await self.perception.perceive(input_data)

        # 2. Attention — filter what is relevant from perception + memory
        focused = await self.attention.select(perception, self.memory)

        # 3. Controller interprets focused input into a goal
        if self.controller:
            goal = await self.controller.interpret(focused)
        else:
            goal = {"goal": focused.get("content", input_data)}

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

        # 7. Learning — record the experience
        experience = Experience(
            result=result,
            error=error,
            feedback=None,
            success=error is None and result is not None,
            context={"goal": goal, "plan": plan},
        )
        await self.learning.update(experience)

        # 8. Store episodic memory
        await self.memory["episodic"].store_event({
            "goal": goal,
            "result": result
        })

        # 9. Controller evaluates whether the goal was satisfied
        if self.controller:
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

        return result