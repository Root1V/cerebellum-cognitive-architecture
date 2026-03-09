"""
LLMClient: implementación del LLM local usando axonium SDK.

Wrappea únicamente axonium.LlamaAdapter.async_chat — el único método
necesario en este proyecto porque permite enviar contexto completo
a través de mensajes estructurados.
"""
import logging

from ..core.llm import LLMClient as LLMClientBase

logger = logging.getLogger("cerebellum.llm")


class LLMClient(LLMClientBase):
    """
    Cliente LLM local basado en axonium SDK.

    Compatible con LLMPlanner, LLMReasoner y LoopReasoner a través
    del contrato LLMClient definido en core/llm.py.

    Ejemplo:
        llm = LLMClient(model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf")
        response = await llm.async_chat([
            {"role": "system", "content": "Eres un asistente de planificación."},
            {"role": "user",   "content": "Analiza el mercado de IA en LATAM."},
        ])
    """

    def __init__(
        self,
        model: str,
        base_url: str | None = None,
        timeout: float = 60.0,
        **kwargs,
    ):
        try:
            from axonium import LlamaAdapter
        except ImportError as exc:
            raise ImportError(
                "El paquete 'axonium' no está instalado. "
                "Instálalo con: uv add axonium"
            ) from exc

        self._adapter = LlamaAdapter(
            model=model,
            base_url=base_url,
            timeout=timeout,
            **kwargs,
        )
        logger.info("LLMClient inicializado con modelo=%s", model)

    async def async_chat(self, messages: list[dict[str, str]], **kwargs) -> str:
        """
        Envía mensajes al LLM local y retorna la respuesta como texto.

        Parameters
        ----------
        messages : lista de mensajes {"role": ..., "content": ...}
        """
        response = await self._adapter.async_chat(messages=messages, **kwargs)
        return response.choices[0].message.content
