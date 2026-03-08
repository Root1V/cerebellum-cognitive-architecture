from typing import Any

from ..core.memory import Memory


class WorkingMemory(Memory):

    def __init__(self):
        self.state: dict[str, Any] = {}

    async def store(self, key: str, value: Any) -> None:
        self.state[key] = value

    async def retrieve(self, key: str) -> Any:
        return self.state.get(key)

    async def update(self, item: dict[str, Any]) -> None:
        if isinstance(item, dict):
            self.state.update(item)