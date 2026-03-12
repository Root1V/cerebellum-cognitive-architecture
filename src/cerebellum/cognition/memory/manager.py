from ..core.memory import Memory

from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .working_memory import WorkingMemory
from .memory_stream import MemoryStream
# ProceduralMemory, GraphMemory, VectorMemory: placeholders

class MemoryManager():
    def __init__(self):
        self.working = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.stream = MemoryStream()
        # self.procedural = ProceduralMemory() # pendiente
        # self.graph = GraphMemory() # pendiente
        # self.vector = VectorMemory() # pendiente

    async def remember(self, key: str, value):
        """
        Almacena el valor siempre en WorkingMemory.
        Luego, según la semántica del valor, lo almacena también en la memoria especializada:
            - Si value es dict y contiene 'goal', 'result', 'timestamp' → EpisodicMemory
            - Si value es dict y contiene 'fact', 'definition', 'document' → SemanticMemory
            - Si value es dict y contiene 'time', 'data' → MemoryStream
        Así, WorkingMemory actúa como buffer/contexto, y el resto como almacenamiento especializado.
        """
        await self.working.store(key, value)
        if isinstance(value, dict):
            if all(k in value for k in ("goal", "result", "timestamp")):
                await self.episodic.store(key, value)
            elif any(k in value for k in ("fact", "definition", "document")):
                await self.semantic.store(key, value)
            elif all(k in value for k in ("time", "data")):
                await self.stream.store(key, value)

    async def recall(self, key: str, memory_type: str = "working"):
        if memory_type == "working":
            return await self.working.retrieve(key)
        elif memory_type == "episodic":
            return await self.episodic.retrieve(key)
        elif memory_type == "semantic":
            return await self.semantic.retrieve(key)
        elif memory_type == "stream":
            return await self.stream.retrieve(key)
        # elif memory_type == "procedural":
        #     return await self.procedural.retrieve(key)
        # elif memory_type == "graph":
        #     return await self.graph.retrieve(key)
        # elif memory_type == "vector":
        #     return await self.vector.retrieve(key)
        else:
            raise ValueError(f"Tipo de memoria desconocido: {memory_type}")

    # Métodos para acceder a cada memoria
    def get_working(self):
        return self.working
    def get_episodic(self):
        return self.episodic
    def get_semantic(self):
        return self.semantic
    def get_stream(self):
        return self.stream
    # def get_procedural(self):
    #     return self.procedural
    # def get_graph(self):
    #     return self.graph
    # def get_vector(self):
    #     return self.vector
