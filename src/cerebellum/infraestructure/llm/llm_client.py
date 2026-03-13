"""
LLMClient: implementación del LLM local usando axonium SDK.

Wrappea únicamente axonium.LlamaAdapter.async_chat. Soporta structured output
mediante Pydantic: si se pasa output_model, el adapter inyecta el schema en el
prompt, pide JSON al LLM y valida la respuesta con Pydantic antes de retornarla.
"""
import json
import logging

from axonium import LlamaAdapter
from pydantic import BaseModel

from .llm import LLM

logger = logging.getLogger("cerebellum.llm")


class LLMClient(LLM):
    """
    Cliente LLM local basado en axonium SDK.
    """

    def __init__(
        self,
        model: str,
        base_url: str | None = None,
        timeout: float = 60.0,
        **kwargs,
    ):
        self._adapter = LlamaAdapter(
            model=model,
            base_url=base_url,
            timeout=timeout,
            **kwargs,
        )
        logger.info("LLMClient inicializado con modelo=%s", model)

    async def think(
        self,
        prompt: str,
        context: str | None = None,
        output_model: type[BaseModel] | None = None,
        **kwargs,
    ) -> str | BaseModel:
        """
        Construye los mensajes, aplica structured output si se pasa output_model,
        llama al SDK y retorna el resultado validado o el string crudo.

        Si output_model está presente:
          - Añade el JSON schema al system prompt para guiar al LLM local.
          - Solicita response_format json_object al SDK.
          - Valida y retorna una instancia Pydantic.
        """
        system_content = context or ""

        if output_model is not None:
            schema_hint = json.dumps(output_model.model_json_schema(), indent=2)
            system_content = (
                f"{system_content}\n\n"
                f"Respond ONLY with a valid JSON object that matches this schema:\n"
                f"{schema_hint}"
            ).strip()
            kwargs["response_format"] = {"type": "json_object"}

        messages: list[dict[str, str]] = []
        if system_content:
            messages.append({"role": "system", "content": system_content})
        messages.append({"role": "user", "content": prompt})

        response = await self._adapter.async_chat(messages=messages, **kwargs)
        raw = response.choices[0].message.content

        if output_model is not None:
            return output_model.model_validate_json(raw)

        return raw
