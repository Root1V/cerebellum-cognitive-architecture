# perception/text_perception.py

from typing import Optional

from ..core.models import InputType, PerceptionResult
from ..core.perception import Perception
from ..neural import NeuralEngine


class TextPerception(Perception):
    """
    Converts raw text into a PerceptionResult.

    If a NeuralEngine is provided, delegates semantic interpretation to it
    (e.g. LLMNeuralEngine for LLM-based, MockNeuralEngine for tests).
    Without a NeuralEngine the result still contains normalized stats but
    no interpretation — useful for lightweight or offline scenarios.
    """

    def __init__(self, neural_engine: Optional[NeuralEngine] = None) -> None:
        self._neural = neural_engine

    async def perceive(self, raw_input: str) -> PerceptionResult:
        text   = raw_input.strip()
        tokens = text.split()

        normalized = {
            "text":      text,
            "length":    len(text),
            "num_words": len(tokens),
        }

        result = PerceptionResult(
            input_type=InputType.TEXT,
            raw=raw_input,
            normalized=normalized,
        )

        if self._neural is not None:
            result.interpretation = await self._neural.interpret(text)

        return result