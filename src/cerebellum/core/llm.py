from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Contrato mínimo para un cliente LLM en cerebellum.

    Única interfaz requerida: async_chat — envía mensajes con contexto completo
    y recibe la respuesta del modelo como string.

    Todas las implementaciones (local, cloud, mock) deben satisfacer este
    contrato para ser intercambiables en LLMPlanner, LLMReasoner y LoopReasoner.
    """

    @abstractmethod
    async def async_chat(self, messages: list[dict[str, str]], **kwargs) -> str:
        """
        Envía una lista de mensajes al LLM y retorna la respuesta como texto.

        Parameters
        ----------
        messages : lista de dicts {"role": "system"|"user"|"assistant", "content": str}
        """
