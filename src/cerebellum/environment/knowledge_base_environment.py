# environment/knowledge_base_environment.py
#
# Entorno basado en base de conocimiento (RAG placeholder).
# Úsalo cuando el agente necesita operar sobre un conjunto de documentos
# o hechos verificados. En producción reemplazaría este store en memoria
# por un vector store (Pinecone, Weaviate, pgvector, etc.).

from typing import Any

from ..core.environment import Environment


class KnowledgeBaseEnvironment(Environment):
    """
    Entorno que expone una base de conocimiento como estado observable.

    Almacena documentos/hechos en memoria. En una implementación real,
    `observe()` haría una query semántica al vector store para retornar
    solo los documentos más relevantes al contexto actual.

    Parameters
    ----------
    documents : Lista de documentos o hechos que componen la base de
                conocimiento inicial del entorno.
    metadata  : Metadatos opcionales del dominio (fuente, fecha, idioma…).

    Example
    -------
    env = KnowledgeBaseEnvironment(
        documents=[
            "AI investment in LATAM grew 34% in 2025.",
            "Brazil and Mexico lead AI adoption in the region.",
            "Fintech is the primary AI use case in Latin America.",
        ],
        metadata={"source": "LATAM Tech Report 2025", "language": "en"},
    )
    """

    def __init__(
        self,
        documents: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self.documents: list[str] = documents or []
        self.metadata: dict[str, Any] = metadata or {}
        self._last_action = None

    def observe(self) -> dict:
        """
        Retorna los documentos disponibles y metadatos del dominio.

        En producción este método recibiría una query y retornaría
        los top-k documentos más relevantes del vector store.
        """
        return {
            "documents": self.documents,
            "metadata": self.metadata,
            "last_action": self._last_action,
        }

    def update(self, action: dict) -> None:
        """
        Registra la acción del agente.
        En producción podría indexar nuevos documentos generados por el agente.
        """
        self._last_action = action

    def add_document(self, document: str) -> None:
        """Agrega un documento a la base de conocimiento en tiempo de ejecución."""
        self.documents.append(document)
