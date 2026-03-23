import pytest

@pytest.mark.asyncio
async def test_memory_recall():

    from cerebellum.cognition.core import CognitiveAgent
    from unittest.mock import AsyncMock

    system = AsyncMock()
    agent = CognitiveAgent(runtime=system)
    
    # Configure the mock to return something the test can check
    system.publish = AsyncMock(side_effect=["", "Lima is the capital of Peru."])

    await agent.run("Remember that the capital of Peru is Lima")
    response = await agent.run("What is the capital of Peru?")

    assert "Lima" in response