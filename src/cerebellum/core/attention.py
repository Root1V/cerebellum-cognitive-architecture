# cognition/attention.py

# La atención decide qué información es relevante.
# Es crucial porque los sistemas cognitivos reciben muchos estímulos.
# Ejemplo:
# 10 documentos
# 100 eventos
# 20 memorias
# La atención selecciona qué usar.

# Ejemplo
# Entrada:
# 50 documentos
# Salida:
# 3 documentos relevantes

from abc import ABC, abstractmethod

from .perception import Perception
from .memory import Memory


class Attention(ABC):

    @abstractmethod
    async def select(self, perception: Perception, memory: Memory):
        """
        Select relevant information for reasoning.
        Returns a filtered/focused subset of the perception output.
        """
        ...