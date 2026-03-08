# memory/working_memory.py

from typing import Any

from ..core.memory import Memory


class WorkingMemory(Memory):

    def __init__(self):
        self.state: dict[str, Any] = {}

    async def store(self, key, value):
        self.state[key] = value

    async def retrieve(self, key):
        return self.state.get(key)

    async def update(self, item):
        if isinstance(item, dict):
            self.state.update(item)