"""
LLMClient: implementación del LLM local usando axonium SDK.

Wrappea únicamente axonium.LlamaAdapter.async_chat. Soporta structured output
mediante Pydantic: si se pasa output_model, el adapter inyecta el schema en el
prompt, pide JSON al LLM y valida la respuesta con Pydantic antes de retornarla.
"""
import json
import logging

from pydantic import BaseModel

from ..core.llm import LLMClient as LLMClientBase

logger = logging.getLogger("cerebellum.llm")


class LLMClient(LLMClientBase):
    """
    Cliente LLM local basado en axonium SDK.

    Ejemplo sin structured output:
        llm = LLMClient(model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf")
        text = await llm.think(
            prompt="Analiza el mercado de IA en LATAM.",
            context="Eres un asistente de planificación.",
        )

    Ejemplo con structured output:
        class PlanStep(BaseModel):
            action: str
            goal: str

        class Plan(BaseModel):
            steps: list[PlanStep]

        plan = await llm.think(
            prompt="Break this goal into steps: ...",
            context="You are a planning assistant.",
            output_model=Plan,
        )
        # plan es una instancia validada de Plan
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
