# examples/research_basic.py
#
# Ejemplo mínimo del ciclo cognitivo completo.
# Usa las implementaciones más simples de cada módulo.

import asyncio

from cerebellum.action import ConsoleAction
from cerebellum.attention import SimpleAttention
from cerebellum.core import CognitiveAgent
from cerebellum.learning import SimpleLearning
from cerebellum.memory import EpisodicMemory, WorkingMemory
from cerebellum.perception import TextPerception
from cerebellum.planners import SimplePlanner
from cerebellum.reasoning import LoopReasoner
from cerebellum.runtime import CognitiveSystem
from cerebellum.environment import TextEnvironment


async def main():

    memory_system = {
        "working": WorkingMemory(),
        "episodic": EpisodicMemory(),
    }

    system = CognitiveSystem(
        perception=TextPerception(),
        attention=SimpleAttention(),
        memory=memory_system,
        planner=SimplePlanner(),
        reasoner=LoopReasoner(),
        action=ConsoleAction(),
        learning=SimpleLearning(),
        environment=TextEnvironment("basic research task"),
    )

    agent = CognitiveAgent(system)

    result = await agent.run("Analyze the AI market")

    print("\nRESULT\n")
    print(result)


asyncio.run(main())