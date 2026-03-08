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


class Attention(ABC):

    @abstractmethod
    async def select(self, perception: dict, memory: dict):
        """
        Select relevant information for reasoning.
        
        Parameters
        ----------
        perception : output dict from Perception.perceive() — structured representation of input.
        memory     : the full memory system dict {"episodic": ..., "working": ..., etc.}.
        
        Returns a filtered/focused subset of the perception output.
        """
        ...