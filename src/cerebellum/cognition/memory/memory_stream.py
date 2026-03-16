# memory/memory_stream.py

from typing import Any

from ..core.memory import Memory



class MemoryStream(Memory):
    """
    MemoryStream
    ------------
    Flujo cronológico de todos los eventos cognitivos.

    Objetivo funcional:
        - Flujo continuo y cronológico de eventos, percepciones, acciones, pensamientos y cambios de estado. 
        - Permite reconstruir el contexto, analizar secuencias, detectar patrones y mantener un historial completo.
        - Inspirado en 'Generative Agents' (Park et al., 2023): simula un "log" cognitivo.

    Uso típico:
        - Agregar eventos con timestamp.
        - Recuperar eventos recientes o filtrar por consulta.
        - Analizar el historial completo para inferir contexto o aprendizaje.

    Métodos:
        - store(key, value): agrega un evento simple.
        - update(item): agrega un evento complejo.
        - add(event): agrega evento con timestamp.
        - retrieve(query): filtra eventos por consulta.
        - recent(n): devuelve los N eventos más recientes.
    """

    def __init__(self):
        self.memories: list[dict] = []

    # --- Memory ABC ---

    async def store(self, key: str, value: Any) -> None:
        self.memories.append({"key": key, "value": value})

    async def retrieve(self, query: str) -> list[Any]:
        return [m for m in self.memories if query in str(m)]

    async def update(self, item: dict) -> None:
        self.memories.append(item)

    # --- Domain-specific API ---

    async def add(self, event: dict) -> None:
        """Agrega un evento con timestamp al stream."""
        self.memories.append({
            "timestamp": event.get("time"),
            "data": event.get("data"),
        })

    async def recent(self, n: int = 5) -> list:
        """Retorna los N eventos más recientes."""
        return self.memories[-n:]