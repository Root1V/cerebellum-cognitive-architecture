import logging
from typing import Optional, Any
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    AttentionOutputPayload,
    ReasoningOutputPayload
)
from cerebellum.cognition.core.models import Plan, PlanStep
from cerebellum.infraestructure.llm.llm import LLM

logger = logging.getLogger("cerebellum.cognition.reasoning.llm")

class LLMPlannerModule(CognitiveModule):
    """
    LLMPlannerModule
    ----------------
    Lóbulo de razonamiento (prefrontal cortex) que genera planes de acción.
    Escucha lo que la atención ha enfocado y utiliza un LLM para decidir los pasos.
    
    Tópicos que escucha:
      - 'attention.focused'
    """

    def __init__(self, name: str = "reasoning.llm", llm_client: Optional[LLM] = None):
        super().__init__(name)
        self.subscriptions.append("attention.focused")
        self.llm = llm_client

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler para resultados de atención enfocada."""
        if message.topic == "attention.focused":
            await self._handle_attention(message)

    async def _handle_attention(self, message: Message) -> None:
        try:
            payload = AttentionOutputPayload(**message.payload)
            
            # Solo razonamos si la relevancia es suficiente (umbral arbitrario por ahora)
            if payload.relevance_score < 0.3:
                logger.debug(f"Ignoring low relevance perception: {payload.relevance_score:.2f}")
                return

            goal_text = payload.focused_result.raw
            logger.info(f"Reasoning about focused input: '{goal_text[:50]}...'")

            # 1. Generar el plan usando el LLM
            plan = await self._generate_plan(goal_text)

            # 2. Emitir el plan listo para ejecución
            output = ReasoningOutputPayload(
                plan=plan,
                goal=str(goal_text),
                metadata={"relevance": payload.relevance_score}
            )
            
            await self.publish("reasoning.plan_ready", output.model_dump(), correlation_id=message.id)
            logger.info(f"Plan generated with {len(plan.steps)} steps.")

        except Exception as e:
            logger.error(f"Error in reasoning/planning: {e}", exc_info=True)

    async def _generate_plan(self, goal: Any) -> Plan:
        """Delega la creación del plan al LLM o usa un fallback estructurado."""
        if self.llm is not None:
            plan = await self.llm.think(
                prompt=f"Break this goal into ordered steps: {goal}",
                context="You are the prefrontal cortex of a cognitive AI. Organize goals into simple actionable steps.",
                output_model=Plan,
            )
            if isinstance(plan, Plan):
                return plan
        
        # Fallback estruturado si no hay LLM o falla
        return Plan(steps=[
            PlanStep(step=1, action="search", goal=f"Find context for: {goal}"),
            PlanStep(step=2, action="process", goal=f"Process information about: {goal}"),
            PlanStep(step=3, action="respond", goal=f"Finalize action for: {goal}"),
        ])
