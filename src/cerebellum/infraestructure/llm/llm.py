from abc import ABC, abstractmethod

from pydantic import BaseModel


class LLM(ABC):
    """
    Contrato base para un cliente LLM en cerebellum.

    Los callers (LLMPlanner, LLMReasoner, LoopReasoner) invocan think(prompt, context).
    El adapter concreto construye el array de mensajes internamente y llama al SDK.

    Si se pasa output_model (clase Pydantic), el adapter aplica structured output
    y retorna una instancia validada del modelo. Sin output_model retorna str.

    Todas las implementaciones (local, cloud, mock) son intercambiables.
    """

    @abstractmethod
    async def think(
        self,
        prompt: str,
        context: str | None = None,
        output_model: type[BaseModel] | None = None,
        **kwargs,
    ) -> str | BaseModel:
        """
        Invoca el LLM con un prompt, contexto opcional y schema de salida opcional.

        Parameters
        ----------
        prompt       : la instrucción o pregunta concreta al modelo
        context      : información de fondo (system role) — memoria, historial,
                       instrucciones del dominio. None si no aplica.
        output_model : clase Pydantic que define la estructura esperada del output.
                       None retorna el string crudo del LLM.
        """

