# memory/episodic_memory.py

from ..core.memory import Memory


class EpisodicMemory(Memory):
    """
    Memoria episódica: almacena experiencias pasadas (eventos, acciones, resultados).
    """

    def __init__(self):
        self.events = []

    # --- Memory ABC ---

    async def store(self, key, value) -> None:
        self.events.append({"key": key, "value": value})

    async def retrieve(self, query) -> list:
        return [e for e in self.events if query in str(e)]

    async def update(self, item) -> None:
        self.events.append(item)

    # --- Domain-specific API ---

    async def store_event(self, event) -> None:
        """Almacena un evento completo (goal + result)."""
        self.events.append(event)

    async def recall(self, query) -> list:
        """Recupera eventos que contengan el query en su representación textual."""
        return [e for e in self.events if query in str(e)]