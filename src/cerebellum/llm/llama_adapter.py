"""
LlamaAdapter: wrapper sobre axonium.LlamaAdapter para integración
con cerebellum-architecture. Expone la interfaz que consumen
LLMPlanner, LLMReasoner y LoopReasoner (método `complete` y `chat`).
"""
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("cerebellum.llm.llama_adapter")


class LlamaAdapter:
    """
    Adapter de LLM local basado en axonium.LlamaAdapter.

    Expone:
        - complete(prompt)          → str   (para LLMPlanner / LLMReasoner)
        - chat(messages, **kwargs)  → str   (interfaz chat)
        - async_chat(messages)      → str   (versión async)

    Ejemplo de uso:
        adapter = LlamaAdapter(model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf")
        result  = await adapter.complete("Break this goal into steps: ...")
    """

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        system_prompt: str = "Eres un asistente de planificación y razonamiento.",
        **kwargs,
    ):
        try:
            from axonium import LlamaAdapter as AxoniumLlamaAdapter
        except ImportError as exc:
            raise ImportError(
                "El paquete 'axonium' no está instalado. "
                "Instálalo con: pip install axonium  o  uv add axonium"
            ) from exc

        self._model = model
        self._system_prompt = system_prompt
        self._adapter = AxoniumLlamaAdapter(
            model=model,
            base_url=base_url,
            timeout=timeout,
            **kwargs,
        )
        logger.info("LlamaAdapter inicializado con modelo=%s", model)

    # ------------------------------------------------------------------
    # Interfaz pública compatible con llm_client de cerebellum
    # ------------------------------------------------------------------

    async def complete(self, prompt: str, **kwargs) -> str:
        """
        Invoca el LLM con un prompt de texto plano.
        Compatible con la interfaz esperada por LLMPlanner y LLMReasoner.
        """
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user",   "content": prompt},
        ]
        return await self._async_chat_raw(messages, **kwargs)

    async def chat(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Invoca el LLM con una lista de mensajes y devuelve el texto."""
        return await self._async_chat_raw(messages, **kwargs)

    def chat_sync(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        """Versión síncrona del chat (usa axonium síncrono)."""
        response = self._adapter.chat(messages=messages, **kwargs)
        return response.choices[0].message.content

    # ------------------------------------------------------------------
    # Privado
    # ------------------------------------------------------------------

    async def _async_chat_raw(self, messages: List[Dict[str, Any]], **kwargs) -> str:
        response = await self._adapter.async_chat(messages=messages, **kwargs)
        return response.choices[0].message.content
