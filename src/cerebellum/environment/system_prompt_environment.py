# environment/system_prompt_environment.py
#
# Entorno basado en system prompt de LLM.
# Úsalo cuando el agente opera sobre un LLM y necesitas definir
# identidad, restricciones y comportamiento del modelo.

from ..core.environment import Environment


class SystemPromptEnvironment(Environment):
    """
    Entorno que representa el contexto de un agente LLM via system prompt.

    El `observe()` retorna el system prompt y las restricciones,
    que el Reasoner puede inyectar directamente al LLM en cada llamada.

    Parameters
    ----------
    system_prompt : Instrucción de sistema que define el rol y comportamiento
                    del agente (equivale al ``system`` message de la API de OpenAI).
    constraints   : Lista de restricciones o reglas que el agente debe respetar.

    Example
    -------
    env = SystemPromptEnvironment(
        system_prompt="You are a financial analyst specialized in LATAM markets.",
        constraints=[
            "Only use verified data sources.",
            "Always cite the year of the data used.",
            "Respond in the same language as the user.",
        ],
    )
    """

    def __init__(self, system_prompt: str, constraints: list[str] | None = None):
        self.system_prompt = system_prompt
        self.constraints = constraints or []
        self._last_action = None

    def observe(self) -> dict:
        """Retorna el system prompt y constraints listos para inyectar al LLM."""
        return {
            "system": self.system_prompt,
            "constraints": self.constraints,
            "last_action": self._last_action,
        }

    def update(self, action: dict) -> None:
        """Registra la acción más reciente del agente."""
        self._last_action = action
