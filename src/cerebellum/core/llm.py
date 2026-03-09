from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Contrato base para un cliente LLM en cerebellum.

    Los callers (LLMPlanner, LLMReasoner, LoopReasoner) invocan think(prompt, context).
    El adapter concreto recibe esos parámetros, construye el array de mensajes
    internamente y llama al SDK — los callers nunca manipulan el formato de mensajes.

    Todas las implementaciones (local, cloud, mock) son intercambiables.
    """

    @abstractmethod
    async def think(self, prompt: str, context: str | None = None, **kwargs) -> str:
        """
        Invoca el LLM con un prompt y contexto opcional.

        Parameters
        ----------
        prompt  : la instrucción o pregunta concreta al modelo
        context : información de fondo (system role) — memoria, historial,
                  instrucciones del dominio. None si no aplica.
        """
