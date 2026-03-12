# memory/episodic_memory.py

from ..core.memory import Memory



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
        self.events: list[dict] = []

    # --- Memory ABC ---

    async def store(self, key: str, value) -> None:
        self.events.append({"key": key, "value": value})

    async def retrieve(self, query: str) -> list:
        return [e for e in self.events if query in str(e)]

    async def update(self, item: dict) -> None:
        self.events.append(item)

    # --- Domain-specific API ---

    async def store_event(self, event: dict) -> None:
        """Almacena un evento completo (goal + result). Alias semántico de update()."""
        await self.update(event)

    async def recall(self, query: str) -> list:
        """Recupera eventos relevantes. Alias semántico de retrieve()."""
        return await self.retrieve(query)
    
    async def recent(self, limit: int = 10) -> list[dict]:
        return self.events[-limit:]
