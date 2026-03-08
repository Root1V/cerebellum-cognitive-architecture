# memory/episodic_memory.py

from ..core.memory import Memory


class EpisodicMemory(Memory):
    """
    Memoria episódica: almacena experiencias pasadas (eventos, acciones, resultados).
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
        """Almacena un evento completo (goal + result)."""
        self.events.append(event)

    async def recall(self, query: str) -> list:
        """Recupera eventos que contengan el query en su representación textual."""
        return [e for e in self.events if query in str(e)]