# perception/text_perception.py

from ..core.perception import Perception

class TextPerception(Perception):

    async def perceive(self, text):

        return {
            "type": "text",
            "content": text
        }