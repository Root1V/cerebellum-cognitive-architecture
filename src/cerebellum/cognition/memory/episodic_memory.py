# memory/episodic_memory.py

import datetime
from typing import Any
import uuid

from pydantic import BaseModel

from ...infraestructure.llm.embedding import Embedding
from ...infraestructure.llm.embedd_client import EmbeddingClient
from ..core.memory import Memory

from pydantic import Field

class EventMemory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    payload: dict
    vector: list[float]
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def __str__(self):
        return f"EventMemory(id={self.id}, payload={self.payload}, vector={self.vector[:3]}..., timestamp={self.timestamp})"


class EpisodicMemory(Memory):
    """
    EpisodicMemory
    --------------
    Memoria episódica cognitiva.

    Objetivo funcional:
        - Almacenar experiencias pasadas de eventos, acciones y resultados.
        - Permite recordar, analizar y consultar el historial de interacciones o situaciones vividas por el agente.
        - Simula un "diario" cognitivo: registro cronológico de lo que ocurrió, cuándo y cómo.

    Uso típico:
        - Guardar eventos relevantes (tareas, resultados, decisiones, contextos).
        - Recuperar eventos por consulta (query) para aprender, razonar o explicar comportamientos.
        - Consultar los eventos más recientes para mantener contexto histórico.

    Métodos:
        - store(key, value): almacena un evento simple.
        - update(item): almacena un evento complejo (dict).
        - retrieve(query): recupera eventos que coinciden con la consulta.
        - store_event(event): alias semántico de update.
        - recall(query): alias semántico de retrieve.
        - recent(limit): devuelve los últimos eventos.
    """

    def __init__(self):
        self._events: list[EventMemory] = []
        self._semantic: Embedding = EmbeddingClient()
        

    # --- Memory ABC ---    
    async def event_to_text(self, event: dict) -> str:
        return ", ".join(f"{k}: {v}" for k, v in event.items())
    
    async def _store(self,  event: EventMemory) -> None:
        text = await self.event_to_text(event.payload)
        vector = await self._semantic.encode(text)
        event.vector = vector
        
        print(f"Storing event: {event}") 
        
        self._events.append(event)
        
    async def store_event(self, event: dict) -> None:
        event_memory = EventMemory(payload=event, vector=[])
        await self._store(event_memory)

    async def store(self, key: str, value) -> None:
        event = EventMemory(payload={key: value}, vector=[])
        await self._store(event)

    async def retrieve(self, query: str) -> list[EventMemory]:
         return [e for e in self._events if query in str(e)]
    
    async def recent(self, limit: int = 10) -> list[EventMemory]:
        return self._events[-limit:]
    
    async def update(self, item: Any) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        """Devuelve el número de eventos almacenados."""
        return len(self._events)
