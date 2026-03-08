# memory/memory_stream.py

from ..core.memory import Memory


class MemoryStream(Memory):
    """
    Memory stream: flujo cronológico de todos los eventos cognitivos.
    Inspirado en el paper 'Generative Agents' (Park et al., 2023).
    """

    def __init__(self):
        self.memories = []

    # --- Memory ABC ---

    async def store(self, key, value) -> None:
        self.memories.append({"key": key, "value": value})

    async def retrieve(self, query) -> list:
        return [m for m in self.memories if query in str(m)]

    async def update(self, item) -> None:
        self.memories.append(item)

    # --- Domain-specific API ---

    async def add(self, event: dict) -> None:
        """Agrega un evento con timestamp al stream."""
        self.memories.append({
            "timestamp": event["time"],
            "data": event["data"]
        })

    async def recent(self, n: int = 5) -> list:
        """Retorna los N eventos más recientes."""
        return self.memories[-n:]