from ..core.attention import Attention


class SimpleAttention(Attention):
    """
    Implementación simple: pasa la percepción completa sin filtrar.
    En una implementación real usaría relevance scoring o embeddings.
    """

    async def select(self, perception: dict, memory: dict) -> dict:
        """
        Retorna la percepción sin modificar.
        memory se recibe para mantener el contrato del ABC pero no se usa aquí.
        """
        return perception