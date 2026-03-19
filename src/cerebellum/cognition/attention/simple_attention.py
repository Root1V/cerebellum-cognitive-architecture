import logging
import math
from typing import List, Optional
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    PerceptionOutputPayload,
    AttentionOutputPayload,
    AttentionSetFocusPayload
)
from cerebellum.infraestructure.llm.embedding import Embedding
from cerebellum.infraestructure.llm.embedd_client import EmbeddingClient

logger = logging.getLogger("cerebellum.cognition.attention.semantic")

class SimpleAttentionModule(CognitiveModule):
    """
    SimpleAttentionModule (ahora con Semántica)
    -------------------------------------------
    Lóbulo de atención que utiliza embeddings para calcular la relevancia 
    de una percepción respecto a un "foco" o consulta actual.
    
    Tópicos que escucha:
      - 'perception.output'
      - 'attention.set_focus'
    """

    def __init__(
        self, 
        name: str = "attention.simple", 
        embedding: Optional[Embedding] = None,
        initial_focus: str = "general interest"
    ):
        super().__init__(name)
        self.subscriptions += ["perception.output", "attention.set_focus"]
        self._embedding_client = embedding or EmbeddingClient()
        self._focus_query = initial_focus
        self._focus_vector: Optional[List[float]] = None

    async def on_start(self, context: CognitiveContext) -> None:
        """Inicializa el foco por defecto."""
        logger.info(f"Attention focus set to: '{self._focus_query}'")
        self._focus_vector = await self._embedding_client.encode(self._focus_query)

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler para resultados de percepción y actualización de foco."""
        if message.topic == "perception.output":
            await self._handle_perception(message)
        elif message.topic == "attention.set_focus":
            await self._handle_set_focus(message)

    async def _handle_set_focus(self, message: Message) -> None:
        try:
            payload = AttentionSetFocusPayload(**message.payload)
            self._focus_query = payload.query
            self._focus_vector = await self._embedding_client.encode(self._focus_query)
            logger.info(f"Attention focus UPDATED to: '{self._focus_query}'")
        except Exception as e:
            logger.error(f"Error updating attention focus: {e}")

    async def _handle_perception(self, message: Message) -> None:
        try:
            payload = PerceptionOutputPayload(**message.payload)
            
            # 1. Obtener texto de la percepción
            raw_text = payload.result.raw
            if not isinstance(raw_text, str):
                raw_text = str(raw_text)

            # 2. Generar embedding de la percepción actual
            perception_vector = await self._embedding_client.encode(raw_text)

            # 3. Calcular similitud con el foco
            score = 1.0
            if self._focus_vector:
                score = self._cosine_similarity(perception_vector, self._focus_vector)
            
            logger.info(f"Perception relevance for focus '{self._focus_query}': {score:.4f}")

            # 4. Emitir resultado enfocado
            output = AttentionOutputPayload(
                focused_result=payload.result,
                relevance_score=float(score),
                metadata={
                    "source_sensor": message.sender,
                    "focus": self._focus_query
                }
            )
            
            await self.publish("attention.focused", output.model_dump(), correlation_id=message.id)

        except Exception as e:
            logger.error(f"Error in attention processing: {e}", exc_info=True)

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Calcula la similitud de coseno. Asume vectores de igual longitud."""
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)