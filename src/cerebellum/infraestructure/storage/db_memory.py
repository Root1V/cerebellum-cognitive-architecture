"""
Contrato abstracto para el almacenamiento de memorias vectoriales.

Todas las implementaciones concretas deben:
- Llamar a ``initialize()`` antes de operar (crea colecciones, índices, etc.).
- Garantizar semántica de upsert en ``store_memory``.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from qdrant_client.http.models import PointStruct


class MemoryStorage(ABC):
    """Interfaz base para backends de almacenamiento de memoria vectorial."""

    @abstractmethod
    async def initialize(self) -> None:
        """
        Inicializa el backend de almacenamiento (crea colecciones, índices, etc.).

        Debe invocarse una vez antes de cualquier operación de lectura/escritura.
        """

    @abstractmethod
    async def store_memory(
        self,
        memory_id: str,
        vector: List[float],
        payload: Optional[dict] = None,
    ) -> None:
        """Persiste una memoria como un punto vectorial (semántica upsert)."""

    @abstractmethod
    async def search_memory(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_payload: Optional[dict] = None,
    ) -> list:
        """Busca las memorias más similares al vector de consulta."""

    @abstractmethod
    async def get_memory_by_id(self, memory_id: str) -> Optional[PointStruct]:
        """Recupera una memoria por su identificador único."""

    @abstractmethod
    async def delete_memory(self, memory_id: str) -> None:
        """Elimina una memoria por su identificador único."""
