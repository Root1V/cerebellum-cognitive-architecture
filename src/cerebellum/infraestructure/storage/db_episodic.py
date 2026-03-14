"""
Implementación del almacenamiento de memoria episódica usando Qdrant como backend vectorial.

Utiliza AsyncQdrantClient para no bloquear el event loop en operaciones I/O,
siguiendo el modelo async del resto de la arquitectura cognitiva.
"""

import logging
from typing import List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointIdsList,
    PointStruct,
    VectorParams,
)

from .db_memory import MemoryStorage

logger = logging.getLogger(__name__)


class MemoryEpisodicStorage(MemoryStorage):
    """
    Almacenamiento vectorial de memoria episódica respaldado por Qdrant.

    Responsabilidad:
        Persistir y recuperar eventos episódicos como vectores en Qdrant,
        habilitando búsqueda semántica por similitud sobre el historial del agente.

    Args:
        host:            Host del servidor Qdrant. Por defecto ``"localhost"``.
        port:            Puerto del servidor Qdrant. Por defecto ``6333``.
        collection_name: Nombre de la colección Qdrant a utilizar.
        vector_size:     Dimensión de los vectores de embedding almacenados.
                         Debe coincidir con el modelo de embedding usado en la capa cognitiva.
                         Por defecto ``384`` (all-MiniLM-L6-v2).
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "memory_episodic",
        vector_size: int = 384,
    ) -> None:
        self._client = AsyncQdrantClient(host=host, port=port)
        self._collection_name = collection_name
        self._vector_size = vector_size

    async def initialize(self) -> None:
        """
        Inicializa el backend: crea la colección si aún no existe.

        Debe llamarse explícitamente después de instanciar la clase,
        ya que ``__init__`` no puede ser async.

        Example::

            storage = MemoryEpisodicStorage()
            await storage.initialize()
        """
        await self._ensure_collection()

    async def _ensure_collection(self) -> None:
        """Crea la colección Qdrant si todavía no existe."""
        existing = await self._client.get_collections()
        names = {c.name for c in existing.collections}

        if self._collection_name not in names:
            await self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(
                    size=self._vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(
                "Colección '%s' creada (vector_size=%d, distance=COSINE).",
                self._collection_name,
                self._vector_size,
            )
        else:
            logger.debug("Colección '%s' ya existe, no se requiere creación.", self._collection_name)

    # ------------------------------------------------------------------ #
    #  MemoryStorage ABC                                                   #
    # ------------------------------------------------------------------ #

    async def store_memory(
        self,
        memory_id: str,
        vector: List[float],
        payload: Optional[dict] = None,
    ) -> None:
        """
        Persiste un evento episódico como un punto en Qdrant.

        Si ya existe un punto con el mismo ``memory_id`` se sobreescribe (upsert).

        Args:
            memory_id: Identificador único del evento (UUID recomendado).
            vector:    Embedding del evento generado por la capa de embedding.
            payload:   Metadatos arbitrarios asociados al evento (timestamp, contexto, etc.).
        """
        point = PointStruct(
            id=memory_id,
            vector=vector,
            payload=payload or {},
        )
        await self._client.upsert(
            collection_name=self._collection_name,
            points=[point],
        )
        logger.debug("Evento almacenado: id=%s payload_keys=%s", memory_id, list((payload or {}).keys()))

    async def search_memory(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_payload: Optional[dict] = None,
    ) -> list:
        """
        Busca los eventos más similares semánticamente al vector de consulta.

        Args:
            query_vector:   Vector de embedding de la consulta.
            top_k:          Número máximo de resultados a devolver.
            filter_payload: Filtro de igualdad exacta sobre los campos del payload.
                            Ejemplo: ``{"session_id": "abc123"}``.

        Returns:
            Lista de ``ScoredPoint`` ordenados por similitud descendente.
        """
        q_filter: Optional[Filter] = None
        if filter_payload:
            q_filter = Filter(
                must=[
                    FieldCondition(key=k, match=MatchValue(value=v))
                    for k, v in filter_payload.items()
                ]
            )

        results = await self._client.search(
            collection_name=self._collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=q_filter,
        )
        logger.debug("Búsqueda completada: top_k=%d resultados=%d", top_k, len(results))
        return results

    async def get_memory_by_id(self, memory_id: str) -> Optional[PointStruct]:
        """
        Recupera un evento episódico por su identificador único.

        Args:
            memory_id: ID del evento a recuperar.

        Returns:
            El ``Record`` correspondiente, o ``None`` si no existe.
        """
        result = await self._client.retrieve(
            collection_name=self._collection_name,
            ids=[memory_id],
        )
        return result[0] if result else None

    async def delete_memory(self, memory_id: str) -> None:
        """
        Elimina un evento episódico por su identificador.

        Args:
            memory_id: ID del evento a eliminar.
        """
        await self._client.delete(
            collection_name=self._collection_name,
            points_selector=PointIdsList(points=[memory_id]),
        )
        logger.debug("Evento eliminado: id=%s", memory_id)

    def __repr__(self) -> str:
        return (
            f"MemoryEpisodicStorage("
            f"collection={self._collection_name!r}, "
            f"vector_size={self._vector_size})"
        )
