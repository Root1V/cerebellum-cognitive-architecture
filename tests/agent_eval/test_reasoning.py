import pytest

@pytest.mark.asyncio
async def test_reasoning_chain():

    from cerebellum.cognition.core import CognitiveAgent
    from unittest.mock import AsyncMock

    system = AsyncMock()
    system.run.return_value = "1 apple remains."
    agent = CognitiveAgent(cognitive_system=system)

    question = "If I have two apples and eat one, how many remain?"

    answer = await agent.run(question)

    assert "1" in answer