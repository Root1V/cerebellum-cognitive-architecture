from ..core.controller import CognitiveController
from ..core.perception import Perception

class SimpleController(CognitiveController):

    async def interpret(self, perception: Perception):

        return {
            "goal": perception["content"]
        }
        
