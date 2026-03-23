import logging
from typing import List, Dict, Any
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    ActionOutputPayload,
    LearningUpdatedPayload
)
from ..core.models import Experience

logger = logging.getLogger("cerebellum.cognition.learning.simple")

class LearningModule(CognitiveModule):
    """
    LearningModule
    --------------
    Módulo que evalúa los resultados de las acciones para optimizar el comportamiento futuro.
    Aprende de los éxitos y errores registrados en 'action.completed'.
    
    Tópicos que escucha:
      - 'action.completed'
      - 'user.feedback' (opcional)
    """

    def __init__(self, name: str = "learning.simple"):
        super().__init__(name)
        self.subscriptions += ["action.completed", "user.feedback"]
        self._experiences: List[Experience] = []

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler para resultados de acciones y feedback."""
        if message.topic == "action.completed":
            await self._handle_action_result(message)
        elif message.topic == "user.feedback":
            await self._handle_feedback(message)

    async def _handle_action_result(self, message: Message) -> None:
        try:
            payload = ActionOutputPayload(**message.payload)
            
            # 1. Crear la experiencia a partir del resultado de la acción
            experience = Experience(
                result=payload.results,
                error=None if payload.success else "Action failed",
                success=payload.success,
                feedback=None,
                context=payload.metadata
            )
            
            self._experiences.append(experience)
            logger.info(f"New experience recorded (Success={payload.success}). Total experiences: {len(self._experiences)}")

            # 2. Generar insights básicos
            insights = await self._calculate_insights()

            # 3. Emitir actualización de aprendizaje
            output = LearningUpdatedPayload(
                experience_id=message.id,
                insights=insights,
                metadata={"goal": payload.metadata.get("goal")}
            )
            await self.publish("learning.updated", output.model_dump(), correlation_id=message.id)

        except Exception as e:
            logger.error(f"Error in learning evaluation: {e}", exc_info=True)

    async def _handle_feedback(self, message: Message) -> None:
        """Actualiza la última experiencia con el feedback recibido."""
        if not self._experiences:
            return
            
        feedback = message.payload.get("feedback")
        self._experiences[-1].feedback = feedback
        logger.info(f"Feedback attached to latest experience: {feedback}")

    async def _calculate_insights(self) -> Dict[str, Any]:
        """Calcula estadísticas de rendimiento."""
        total = len(self._experiences)
        if total == 0:
            return {"success_rate": 0.0, "total": 0}
            
        successes = sum(1 for e in self._experiences if e.success)
        return {
            "total": total,
            "success_rate": successes / total,
            "trend": "improving" if successes > (total / 2) else "neutral"
        }