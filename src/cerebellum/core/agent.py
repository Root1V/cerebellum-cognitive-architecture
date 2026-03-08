# core/agent.py
from typing import Any

from ..runtime.cognitive_system import CognitiveSystem


class CognitiveAgent:

    def __init__(self, cognitive_system: CognitiveSystem) -> None:
        self.system: CognitiveSystem = cognitive_system

    async def run(self, task: str) -> Any:
        return await self.system.run(task)