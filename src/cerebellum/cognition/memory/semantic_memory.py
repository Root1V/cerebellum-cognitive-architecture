import logging
from typing import Any, Dict
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    MemoryStorePayload, 
    MemoryRecallPayload, 
    MemoryAvailablePayload
)

logger = logging.getLogger("cerebellum.cognition.memory.semantic")

class SemanticMemory(CognitiveModule):
    """
    SemanticMemory (Memoria Semántica)
    ---------------------------------
    Módulo cognitivo que almacena conocimiento general, hechos y conceptos.
    A diferencia de la episódica, esta memoria es atemporal y estructurada.
    
    Tópicos que escucha:
      - 'memory.store' (si scope == 'semantic')
      - 'memory.recall' (si scope == 'semantic')
    """

    def __init__(self, name: str = "memory.semantic"):
        super().__init__(name)
        self.subscriptions += ["memory.store", "memory.recall"]
        self.knowledge: Dict[str, Any] = {}

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """
        Handler principal para peticiones de memoria semántica.
        """
        if message.topic == "memory.store":
            await self._handle_store(message)
        
        elif message.topic == "memory.recall":
            await self._handle_recall(message)

    async def _handle_store(self, message: Message) -> None:
        try:
            payload = MemoryStorePayload(**message.payload)
            if payload.scope == "semantic":
                self.knowledge[payload.key] = payload.value
                logger.debug(f"Knowledge stored in semantic memory: {payload.key}")
                
                await self.publish("memory.stored", {
                    "key": payload.key,
                    "scope": "semantic"
                }, correlation_id=message.id)
        except Exception as e:
            logger.error(f"Error storing in semantic memory: {e}")

    async def _handle_recall(self, message: Message) -> None:
        try:
            payload = MemoryRecallPayload(**message.payload)
            if payload.scope == "semantic":
                val = self.knowledge.get(payload.key)
                found = payload.key in self.knowledge
                
                logger.debug(f"Recall from semantic memory: {payload.key} (Found: {found})")
                
                response = MemoryAvailablePayload(
                    id=message.id,
                    data=val,
                    found=found,
                    metadata={"source": "semantic"}
                )
                await self.publish("memory.available", response.model_dump())
        except Exception as e:
            logger.error(f"Error recalling from semantic memory: {e}")

    # Compatibilidad temporal
    async def store(self, key: str, value: Any) -> None:
        self.knowledge[key] = value

    async def retrieve(self, query: str) -> Any:
        return self.knowledge.get(query)

    async def update(self, item: dict) -> None:
        if isinstance(item, dict):
            self.knowledge.update(item)