import pytest

@pytest.mark.asyncio
async def test_planning():

    from src.agent import CognitiveAgent

    agent = CognitiveAgent()

    response = await agent.run(
        "Create a plan to organize a conference"
    )

    assert "step" in response.lower()