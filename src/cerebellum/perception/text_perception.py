# perception/text_perception.py

from ..core.perception import Perception

class TextPerception(Perception):

    async def process(self, text):

        return {
            "type": "text",
            "content": text
        }