# environment/text_environment.py
#
# Entorno de texto simple: adecuado para desarrollo y testing.
# Encapsula un contexto estático como string descriptivo del dominio.

from ..core.environment import Environment


class TextEnvironment(Environment):
    """
    Entorno de texto simple.

    Úsalo para desarrollo, tests o cuando el contexto del mundo
    pueda describirse como un string estático.

    Parameters
    ----------
    context : Descripción textual del dominio / contexto del mundo en el
              que opera el agente. NO es la tarea — es el estado del entorno.

    Example
    -------
    env = TextEnvironment(
        "Domain: Latin American technology market. Year: 2026."
    )
    """

    def __init__(self, context: str):
        self.context = context
        self._last_action = None

    def observe(self) -> dict:
        """Retorna el estado actual del entorno como dict estructurado."""
        return {
            "context": self.context,
            "last_action": self._last_action,
        }

    def update(self, action: dict) -> None:
        """Registra la acción ejecutada por el agente."""
        self._last_action = action
        print("Environment received:", action)
