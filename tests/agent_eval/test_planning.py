import pytest

@pytest.mark.asyncio
async def test_planning():

    from cerebellum.cognition.core import CognitiveAgent
    from unittest.mock import AsyncMock

    system = AsyncMock()
    system.publish = AsyncMock(return_value="Step 1: Do something")
    agent = CognitiveAgent(runtime=system)

    response = await agent.run(
        "Create a plan to organize a conference"
    )

    assert "step" in response.lower()