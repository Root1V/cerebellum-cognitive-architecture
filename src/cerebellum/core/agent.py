# core/agent.py
from ..runtime.cognitive_system import CognitiveSystem

class CognitiveAgent:

    def __init__(self, cognitive_system: CognitiveSystem):
        self.system: CognitiveSystem = cognitive_system
    
    async def run(self, task):

        self.system.set_goal(task)

        while not self.system.is_finished():
            self.system.step()

        return self.system.get_result()