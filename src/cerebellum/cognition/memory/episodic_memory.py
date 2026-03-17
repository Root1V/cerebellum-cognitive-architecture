import logging
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from cerebellum.cognition.runtime.cognitive_runtime import CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.runtime.protocols import (
    MemoryStorePayload,
    MemoryRecallPayload,
    MemorySearchPayload,
    MemoryAvailablePayload
)

from ...infraestructure.storage.db_memory import MemoryStorage
from ...infraestructure.storage.db_episodic import MemoryEpisodicStorage
from ...infraestructure.llm.embedding import Embedding
from ...infraestructure.llm.embedd_client import EmbeddingClient

logger = logging.getLogger("cerebellum.cognition.memory.episodic")

class EpisodicMemory(CognitiveModule):
    """
    EpisodicMemory (Memoria Episódica)
    ---------------------------------
    Módulo cognitivo que almacena experiencias pasadas (eventos).
    Utiliza almacenamiento vectorial (Qdrant) para permitir búsqueda por similitud.
    
    Tópicos que escucha:
      - 'memory.store' (si scope == 'episodic')
      - 'memory.recall' (si scope == 'episodic')
      - 'memory.search' (búsqueda semántica)
    """

    def __init__(
        self, 
        name: str = "memory.episodic",
        embedding: Optional[Embedding] = None,
        storage: Optional[MemoryStorage] = None
    ):
        super().__init__(name)
        self.subscriptions += ["memory.store", "memory.recall", "memory.search"]
        self._semantic: Embedding = embedding or EmbeddingClient()
        self._storage: MemoryStorage = storage or MemoryEpisodicStorage()
        self._initialized = False

    async def on_start(self, context: CognitiveContext) -> None:
        """Inicializa el storage al arrancar el módulo."""
        if not self._initialized:
            logger.info("Initializing Episodic Memory storage...")
            await self._storage.initialize()
            self._initialized = True

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        """Handler principal de mensajes episódicos."""
        if message.topic == "memory.store":
            await self._handle_store(message)
        elif message.topic == "memory.recall":
            await self._handle_recall(message)
        elif message.topic == "memory.search":
            await self._handle_search(message)

    async def _event_to_text(self, payload: Dict[str, Any]) -> str:
        """Convierte un payload a texto para generar el embedding."""
        # Estrategia simple por ahora: concatenar claves y valores
        return ", ".join(f"{k}: {v}" for k, v in payload.items())

    async def _handle_store(self, message: Message) -> None:
        try:
            payload = MemoryStorePayload(**message.payload)
            if payload.scope == "episodic":
                # 1. Generar texto representativo
                text = await self._event_to_text(payload.value if isinstance(payload.value, dict) else {"content": payload.value})
                
                # 2. Generar embedding
                vector = await self._semantic.encode(text)
                
                # 3. Guardar en Qdrant
                # Usamos el key como ID si es un UUID válido, o generamos uno nuevo ligado al mensaje
                memory_id = payload.key if payload.key else str(uuid.uuid4())
                
                # Enriquecemos el payload con metadatos útiles
                enriched_value = payload.value if isinstance(payload.value, dict) else {"data": payload.value}
                enriched_value["timestamp"] = enriched_value.get("timestamp", datetime.now().isoformat())
                enriched_value["_source_msg_id"] = message.id
                
                await self._storage.store_memory(memory_id, vector, enriched_value)
                
                logger.debug(f"Event stored in episodic memory: {memory_id}")
                await self.publish("memory.stored", {
                    "key": memory_id,
                    "scope": "episodic"
                }, correlation_id=message.id)
                
        except Exception as e:
            logger.error(f"Error storing in episodic memory: {e}", exc_info=True)

    async def _handle_recall(self, message: Message) -> None:
        try:
            payload = MemoryRecallPayload(**message.payload)
            if payload.scope == "episodic":
                record = await self._storage.get_memory_by_id(payload.key)
                
                found = False
                data = None
                if record is not None:
                    found = True
                    data = record.payload if hasattr(record, 'payload') else None
                
                response = MemoryAvailablePayload(
                    id=message.id,
                    data=data,
                    found=found,
                    metadata={"source": "episodic", "id": payload.key}
                )
                await self.publish("memory.available", response.model_dump())
        except Exception as e:
            logger.error(f"Error recalling from episodic memory: {e}", exc_info=True)

    async def _handle_search(self, message: Message) -> None:
        try:
            payload = MemorySearchPayload(**message.payload)
            
            # 1. Generar vector de la consulta
            query_vector = await self._semantic.encode(payload.query)
            
            # 2. Buscar en Qdrant
            results = await self._storage.search_memory(
                query_vector, 
                top_k=payload.limit,
                filter_payload=payload.metadata_filter
            )
            
            # 3. Formatear resultados
            found_data = []
            for res in results:
                found_data.append({
                    "score": res.score,
                    "payload": res.payload,
                    "id": res.id
                })
            
            response = MemoryAvailablePayload(
                id=message.id,
                data=found_data,
                found=len(found_data) > 0,
                metadata={"source": "episodic", "search_query": payload.query}
            )
            await self.publish("memory.available", response.model_dump())
            
        except Exception as e:
            logger.error(f"Error searching in episodic memory: {e}", exc_info=True)

    @property
    def size(self) -> int:
        # Nota: Qdrant no devuelve el tamaño fácilmente sin una llamada asíncrona dedicada
        return -1 # Deshabilitado para sync property
