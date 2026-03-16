from typing import Any

from ..core.memory import Memory


class WorkingMemory(Memory):

    """
    WorkingMemory
    --------------
    Memoria de trabajo cognitiva.

    Objetivo funcional:
        - Almacenar información temporal y activa durante el razonamiento, planificación o ejecución de tareas.
        - Permite manipular, consultar y actualizar datos relevantes al contexto inmediato.
        - Simula la "memoria RAM" de un sistema cognitivo: acceso rápido, datos volátiles, soporte para operaciones en curso.

    Uso típico:
        - Guardar variables, resultados intermedios, contexto de la tarea actual.
        - Recuperar información para tomar decisiones o continuar procesos.
        - Actualizar el estado conforme cambian los datos o se reciben nuevos inputs.

    Métodos:
        - store(key, value): almacena un dato.
        - retrieve(key): recupera un dato por clave.
        - update(item): actualiza múltiples datos.
    """

    def __init__(self):
        self._state: dict[str, Any] = {}

    async def store(self, key: str, value: Any) -> None:
        self._state[key] = value

    async def retrieve(self, query: str) -> Any:
        return self._state.get(query)

    async def update(self, item: dict[str, Any]) -> None:
        if isinstance(item, dict):
            self._state.update(item)