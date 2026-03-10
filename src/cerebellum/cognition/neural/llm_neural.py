from ..core.models import NeuralInterpretation
from ..neural.neural import NeuralEngine
from ...infraestructure.llm.llm import LLMClient

_SYSTEM_PROMPT = (
    "You are a perception module in a cognitive AI architecture.\n"
    "Given a raw text input, return a structured interpretation with:\n"
    "- intent: the high-level intent ('query', 'command', or 'statement')\n"
    "- entities: a dict with 'named' (list of named entities) and 'numbers' (list of numeric values as strings)\n"
    "- summary: a brief one-sentence summary of the input\n"
    "- extracted_facts: a list of facts, each with 'kind', 'name', 'value', 'confidence' and 'metadata'\n"
    "- confidence: your overall confidence in the interpretation (0.0 to 1.0)\n"
    "Respond only with the JSON matching the schema provided."
)


class LLMNeuralEngine(NeuralEngine):
    """NeuralEngine backed by an LLMClient — uses structured output to produce NeuralInterpretation."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    async def interpret(self, text: str) -> NeuralInterpretation:
        return await self._llm.think(
            prompt=f'Interpret this input: "{text}"',
            context=_SYSTEM_PROMPT,
            output_model=NeuralInterpretation,
        )
