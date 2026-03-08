from ..core.attention import Attention
from ..core.perception import Perception
from ..core.memory import Memory


class SimpleAttention(Attention):
    """
    Implementación simple: pasa la percepción completa sin filtrar.
    En una implementación real usaría relevance scoring o embeddings.
    """

    async def select(self, perception: Perception, memory: Memory) -> dict:
        """
        Retorna la percepción sin modificar.
        memory se recibe para mantener el contrato del ABC pero no se usa aquí.
        """
        return perception