import logging
from typing import Dict, Optional
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    AttentionOutputPayload,
    ReasoningOutputPayload
)
from cerebellum.cognition.core.models import Plan, PlanStep
from cerebellum.tools.tool import Tool

logger = logging.getLogger("cerebellum.cognition.reasoning.simple")

class SimplePlannerModule(CognitiveModule):
    """
    SimplePlannerModule
    -------------------
    Lóbulo de planificación básico que utiliza herramientas (Tools) registradas
    para generar un plan secuencial directo.
    
    Tópicos que escucha:
      - 'attention.focused'
    """

    def __init__(self, name: str = "reasoning.simple", tools: Optional[Dict[str, Tool]] = None):
        super().__init__(name)
        self.subscriptions.append("attention.focused")
        self.tools: Dict[str, Tool] = tools or {}

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "attention.focused":
            await self._handle_attention(message)

    async def _handle_attention(self, message: Message) -> None:
        try:
            payload = AttentionOutputPayload(**message.payload)
            if payload.relevance_score < 0.3:
                return

            goal_text = payload.focused_result.raw
            logger.info(f"Generating simple plan for: '{goal_text[:30]}...'")

            if self.tools:
                steps = [
                    PlanStep(step=i + 1, action=name, goal=str(goal_text))
                    for i, name in enumerate(self.tools)
                ]
            else:
                steps = [PlanStep(step=1, action="process", goal=str(goal_text))]

            plan = Plan(steps=steps)
            
            output = ReasoningOutputPayload(
                plan=plan,
                goal=str(goal_text),
                metadata={"plan_type": "simple"}
            )
            
            await self.publish("reasoning.plan_ready", output.model_dump(), correlation_id=message.id)

        except Exception as e:
            logger.error(f"Error in simple planner: {e}")
