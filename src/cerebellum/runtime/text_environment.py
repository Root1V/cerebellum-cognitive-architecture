
from ..core.environment import Environment


class TextEnvironment(Environment):
    """
    Entorno de texto simple.
    observe() expone el estado actual como un dict estructurado.
    update() registra las acciones recibidas del agente.
    """

    def __init__(self, text: str):
        self.text = text
        self._last_action = None

    def observe(self) -> dict:
        """Retorna el estado actual del entorno como dict estructurado."""
        return {"input": self.text, "last_action": self._last_action}

    def update(self, action: dict) -> None:
        """Registra la acción ejecutada por el agente y actualiza el estado."""
        self._last_action = action
        print("Environment received:", action)
        