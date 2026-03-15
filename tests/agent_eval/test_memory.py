import pytest

@pytest.mark.asyncio
async def test_memory_recall():

    from src.agent import CognitiveAgent

    agent = CognitiveAgent()

    await agent.run("Remember that the capital of Peru is Lima")

    response = await agent.run("What is the capital of Peru?")

    assert "Lima" in response