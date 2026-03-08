# perception/text_perception.py

from ..core.perception import Perception


class TextPerception(Perception):

    async def perceive(self, text: str) -> dict:
        return {
            "type": "text",
            "content": text
        }