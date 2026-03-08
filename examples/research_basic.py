# examples/research_agent.py

import asyncio

from cerebellum.runtime import CognitiveSystem
from cerebellum.perception import TextPerception
from cerebellum.planners import SimplePlanner
from cerebellum.reasoning import LLMReasoner
from cerebellum.memory import WorkingMemory
from cerebellum.core import CognitiveAgent


async def main():

    perception = TextPerception()
    memory = WorkingMemory()
    planner = SimplePlanner()
    reasoner = LLMReasoner(llm_client=None)

    system = CognitiveSystem(
        perception=perception,
        controller=None,
        memory=memory,
        planner=planner,
        reasoner=reasoner,
        tools=[]
    )

    agent = CognitiveAgent(system)

    result = await agent.run(
        "Analyze the AI market"
    )

    print(result)


asyncio.run(main())