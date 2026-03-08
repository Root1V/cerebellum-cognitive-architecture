# core/agent.py
from ..runtime.cognitive_system import CognitiveSystem

class CognitiveAgent:

    def __init__(self, cognitive_system: CognitiveSystem):
        self.system = cognitive_system

    async def run(self, task):

        result = await self.system.run(task)

        return result