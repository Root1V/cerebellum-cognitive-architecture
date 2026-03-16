import pytest

@pytest.mark.asyncio
async def test_planning():

    from cerebellum.cognition.core import CognitiveAgent
    from unittest.mock import AsyncMock

    system = AsyncMock()
    system.run.return_value = "Step 1: Do something"
    agent = CognitiveAgent(cognitive_system=system)

    response = await agent.run(
        "Create a plan to organize a conference"
    )

    assert "step" in response.lower()