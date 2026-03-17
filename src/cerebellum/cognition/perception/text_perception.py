import logging
from typing import Optional
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    PerceptionProcessPayload,
    PerceptionOutputPayload
)
from ..core.models import InputType, PerceptionResult
from ..neural import NeuralEngine

logger = logging.getLogger("cerebellum.cognition.perception.text")

class TextPerceptionModule(CognitiveModule):
    """
    TextPerceptionModule
    --------------------
    Módulo cognitivo que convierte texto bruto en una estructura de percepción.
    Si se proporciona un NeuralEngine, delega la interpretación semántica.
    
    Tópicos que escucha:
      - 'perception.process' (si input_type == 'text')
    """

    def __init__(self, name: str = "perception.text", neural_engine: Optional[NeuralEngine] = None):
        super().__init__(name)
        self.subscriptions.append("perception.process")
        self._neural = neural_engine

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler para peticiones de percepción de texto."""
        if message.topic == "perception.process":
            await self._handle_process(message)

    async def _handle_process(self, message: Message) -> None:
        try:
            payload = PerceptionProcessPayload(**message.payload)
            
            # Solo procesamos si el tipo es texto (o por defecto)
            if payload.input_type != "text":
                return

            raw_input = str(payload.raw_data)
            text = raw_input.strip()
            tokens = text.split()

            normalized = {
                "text": text,
                "length": len(text),
                "num_words": len(tokens),
            }

            result = PerceptionResult(
                input_type=InputType.TEXT,
                raw=raw_input,
                normalized=normalized,
            )

            if self._neural is not None:
                logger.debug(f"Interpreting text with neural engine: {text[:50]}...")
                result.interpretation = await self._neural.interpret(text)

            # Publicamos el lóbulo de salida
            output_payload = PerceptionOutputPayload(result=result)
            await self.publish("perception.output", output_payload.model_dump(), correlation_id=message.id)
            
            logger.info(f"Perception completed for input (length={len(text)})")

        except Exception as e:
            logger.error(f"Error in text perception: {e}", exc_info=True)