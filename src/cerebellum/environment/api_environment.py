# environment/api_environment.py
#
# Entorno que obtiene su estado desde una API externa.
# Úsalo cuando el agente opera sobre datos en tiempo real
# (precios de mercado, sensores, feeds de noticias, etc.).
#
# NOTA: La implementación actual es un placeholder síncrono.
# En producción reemplaza _fetch() con httpx.AsyncClient o requests.

from typing import Any

from ..cognition.core.environment import Environment


class APIEnvironment(Environment):
    """
    Entorno cuyo estado proviene de una API externa.

    `observe()` llama a `_fetch()` para obtener el estado actual del mundo.
    Sobrescribe `_fetch()` en una subclase para conectar a cualquier API real.

    Parameters
    ----------
    base_url  : URL base del endpoint que expone el estado del entorno.
    headers   : Headers HTTP opcionales (autenticación, content-type, etc.).
    fallback  : Estado que se retorna si la API no está disponible.

    Example
    -------
    env = APIEnvironment(
        base_url="https://api.market-data.com/latam/state",
        headers={"Authorization": "Bearer <token>"},
        fallback={"status": "unavailable"},
    )

    # Subclase con fetch real:
    class LiveMarketEnvironment(APIEnvironment):
        def _fetch(self) -> dict:
            import httpx
            return httpx.get(self.base_url, headers=self.headers).json()
    """

    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        fallback: dict[str, Any] | None = None,
    ):
        self.base_url = base_url
        self.headers = headers or {}
        self.fallback = fallback or {"status": "unavailable"}
        self._last_action = None

    def _fetch(self) -> dict:
        """
        Obtiene el estado actual del entorno desde la API.
        Placeholder — retorna el fallback. Sobreescribir en producción.
        """
        return {**self.fallback, "source": self.base_url}

    def observe(self) -> dict:
        """Retorna el estado actual obtenido de la API."""
        state = self._fetch()
        state["last_action"] = self._last_action
        return state

    def update(self, action: dict) -> None:
        """
        Registra la acción ejecutada por el agente.
        En producción podría hacer un POST a la API para aplicar el efecto.
        """
        self._last_action = action
