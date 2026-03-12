# maybe vector database
# maybe knowledge graph

from typing import Any

from ..core.memory import Memory



class SemanticMemory(Memory):
    """
    SemanticMemory
    --------------
    Memoria semántica cognitiva.

    Objetivo funcional:
        - Almacenar y organizar conocimiento general, hechos, conceptos, relaciones y documentos.
        - Permite acceder a información estructurada sobre el mundo, reglas, definiciones y bases de conocimiento.
        - Simula una "base de datos" cognitiva: conocimiento estable, no ligado a experiencias puntuales.

    Uso típico:
        - Guardar hechos, definiciones, relaciones, documentos, reglas.
        - Recuperar información por clave o consulta semántica.
        - Actualizar el conocimiento conforme se aprende o se recibe nueva información.

    Métodos:
        - store(key, value): almacena un hecho o concepto.
        - retrieve(query): recupera información por clave.
        - update(item): actualiza múltiples hechos/conceptos.
    """

    def __init__(self):
        self.knowledge: dict[str, Any] = {}

    async def store(self, key: str, value) -> None:
        self.knowledge[key] = value

    async def retrieve(self, query: str) -> Any:
        return self.knowledge.get(query)

    async def update(self, item: dict) -> None:
        if isinstance(item, dict):
            self.knowledge.update(item)