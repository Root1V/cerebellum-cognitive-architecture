import logging
from typing import Any, Dict
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    MemoryStorePayload, 
    MemoryRecallPayload, 
    MemoryAvailablePayload
)

logger = logging.getLogger("cerebellum.cognition.memory.working")

class WorkingMemory(CognitiveModule):
    """
    WorkingMemory (Memoria de Trabajo)
    ---------------------------------
    Módulo cognitivo inspirado en la RAM humana. Almacena el contexto inmediato 
    y volátil necesario para el razonamiento actual.
    
    Tópicos que escucha:
      - 'memory.store' (si scope == 'working')
      - 'memory.recall' (si scope == 'working')
    """

    def __init__(self, name: str = "memory.working"):
        super().__init__(name)
        self.subscriptions += ["memory.store", "memory.recall"]
        self._state: Dict[str, Any] = {}

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """
        Handler principal para peticiones de memoria de trabajo.
        """
        if message.topic == "memory.store":
            await self._handle_store(message)
        
        elif message.topic == "memory.recall":
            await self._handle_recall(message)

    async def _handle_store(self, message: Message) -> None:
        try:
            payload = MemoryStorePayload(**message.payload)
            if payload.scope == "working":
                self._state[payload.key] = payload.value
                logger.debug(f"Stored in working memory: {payload.key}")
                
                # Emitimos confirmación (opcional pero útil para seguimiento)
                await self.publish("memory.stored", {
                    "key": payload.key,
                    "scope": "working"
                }, correlation_id=message.id)
        except Exception as e:
            logger.error(f"Error storing in working memory: {e}")

    async def _handle_recall(self, message: Message) -> None:
        try:
            payload = MemoryRecallPayload(**message.payload)
            if payload.scope == "working":
                val = self._state.get(payload.key)
                found = payload.key in self._state
                
                logger.debug(f"Recall from working memory: {payload.key} (Found: {found})")
                
                # Publicamos el resultado
                response_payload = MemoryAvailablePayload(
                    id=message.id,
                    data=val,
                    found=found
                )
                await self.publish("memory.available", response_payload.model_dump())
        except Exception as e:
            logger.error(f"Error recalling from working memory: {e}")

    # Métodos heredados del modelo anterior para compatibilidad temporal si fuera necesario
    async def store(self, key: str, value: Any) -> None:
        self._state[key] = value

    async def retrieve(self, query: str) -> Any:
        return self._state.get(query)