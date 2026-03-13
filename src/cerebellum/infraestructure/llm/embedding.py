from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class Embedding(ABC):
    """
    Contrato base para un cliente de embeddings en cerebellum.
    """

    @abstractmethod
    async def encode(
        self,
        text: str | None = None,        
    ) -> Any:
        """
        Genera un embedding vectorial a partir de un input textual.
        """

