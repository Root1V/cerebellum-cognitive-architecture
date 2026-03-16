
import logging
from typing import Any

from sentence_transformers import SentenceTransformer
from .embedding import Embedding

logger = logging.getLogger("cerebellum.llm")


class EmbeddingClient(Embedding):
    """
    Interfaz para clientes de generación de embeddings vectoriales.
    Este contrato define el método encode(text) que toma un string de entrada
    y retorna un vector numérico (embedding) que representa el significado semántico
    del texto. 
    """
    def __init__(self, model_name: str | None = None):
        """
        Inicializa el cliente de embeddings con un modelo específico.

        Parameters
        ----------
        model_name : El nombre o identificador del modelo de embeddings a usar.
        """
        self._model_name = model_name or "all-MiniLM-L6-v2"
        self._model = SentenceTransformer(self._model_name)

        logger.info("EmbeddingClient inicializado con modelo=%s", self._model_name)

    async def encode(
        self,
        text: str | None = None,        
    ) -> Any:
        """
        Genera un embedding vectorial a partir de un input textual.

        Parameters
        ----------
        text : El texto de entrada que se desea convertir en un embedding vectorial.

        Returns
        -------
        Un vector numérico (embedding) que representa el significado semántico del texto.
        """
        vectors = self._model.encode(text or "")
        logger.info("Embedding generado para texto=%s", text)
        logger.debug("Vector embedding: %s", vectors[:5])
        
        return vectors.tolist()