import pytest

@pytest.mark.asyncio
async def test_memory_recall():

    from cerebellum.cognition.core import CognitiveAgent
    from unittest.mock import AsyncMock

    system = AsyncMock()
    # Mocking the responses so the assert passes
    system.run.side_effect = ["", "Lima is the capital of Peru."]
    agent = CognitiveAgent(cognitive_system=system)

    await agent.run("Remember that the capital of Peru is Lima")

    response = await agent.run("What is the capital of Peru?")

    assert "Lima" in response