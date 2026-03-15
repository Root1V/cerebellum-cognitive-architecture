import pytest

@pytest.mark.asyncio
async def test_reasoning_chain():

    from src.agent import CognitiveAgent

    agent = CognitiveAgent()

    question = "If I have two apples and eat one, how many remain?"

    answer = await agent.run(question)

    assert "1" in answer