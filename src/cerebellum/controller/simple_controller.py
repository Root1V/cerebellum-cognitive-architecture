from ..core.controller import CognitiveController
from ..core.perception import Perception

class SimpleController(CognitiveController):

    async def interpret(self, perception: Perception):

        return [
            {"step": "search_market_data", "goal": perception["content"]},
            {"step": "analyze_trends", "goal": perception["content"]},
            {"step": "generate_summary", "goal": perception["content"]},
        ]
        
