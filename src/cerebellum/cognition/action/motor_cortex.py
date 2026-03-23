import logging
from typing import Dict, List, Optional
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    ReasoningOutputPayload,
    ActionOutputPayload
)
from cerebellum.cognition.core.models import ActionResult
from cerebellum.tools.tool import Tool

logger = logging.getLogger("cerebellum.cognition.action.motor")

class MotorCortexModule(CognitiveModule):
    """
    MotorCortexModule
    -----------------
    Lóbulo de acción (corteza motora) que ejecuta los planes de razonamiento.
    Interactúa con herramientas (Tools) y el entorno exterior.
    
    Tópicos que escucha:
      - 'reasoning.plan_ready'
    """

    def __init__(self, name: str = "action.motor", tools: Optional[Dict[str, Tool]] = None):
        super().__init__(name)
        self.subscriptions.append("reasoning.plan_ready")
        self.tools: Dict[str, Tool] = tools or {}

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler para recibir planes listos para ejecución."""
        if message.topic == "reasoning.plan_ready":
            await self._handle_plan(message)

    async def _handle_plan(self, message: Message) -> None:
        try:
            payload = ReasoningOutputPayload(**message.payload)
            plan = payload.plan
            logger.info(f"MotorCortex received plan with {len(plan.steps)} steps for goal: '{payload.goal[:30]}...'")

            results: List[ActionResult] = []
            overall_success = True

            for step in plan.steps:
                logger.info(f"🚀 Executing Step {step.step}: {step.action} (Goal: {step.goal})")
                
                result = await self._execute_step(step.action, step.goal)
                results.append(result)
                
                if not result.success:
                    overall_success = False
                    logger.warning(f"❌ Step {step.step} failed. Metadata: {result.metadata}")
                    # En modelos más complejos aquí podríamos disparar un lóbulo de aprendizaje
                else:
                    logger.info(f"✅ Step {step.step} completed successfully.")

            # Publicamos el reporte final de ejecución
            output = ActionOutputPayload(
                results=results,
                success=overall_success,
                metadata={"goal": payload.goal}
            )
            await self.publish("action.completed", output.model_dump(), correlation_id=message.id)
            logger.info(f"🏁 Execution finished. Success: {overall_success}")

        except Exception as e:
            logger.error(f"Error in motor cortex execution: {e}", exc_info=True)

    async def _execute_step(self, action_name: str, goal: str) -> ActionResult:
        """Busca una herramienta por nombre o simula ejecución vía logs."""
        tool = self.tools.get(action_name)
        
        try:
            if tool:
                output = await tool.execute(goal=goal)
                return ActionResult(action=action_name, success=True, output=output)
            else:
                # Simulación por defecto para el demo
                logger.debug(f"Tool '{action_name}' not found. Simulating...")
                return ActionResult(
                    action=action_name, 
                    success=True, 
                    output=f"Simulated execution of {action_name}",
                    metadata={"mock": True}
                )
        except Exception as e:
            return ActionResult(
                action=action_name, 
                success=False, 
                metadata={"error": str(e)}
            )

