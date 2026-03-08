# El flujo será:

# User Task
#  ↓
# Perception
#  ↓
# Attention
#  ↓
# Memory Retrieval
#  ↓
# Planner
#  ↓
# Reasoner
#  ↓
# Tools
#  ↓
# Action
#  ↓
# Learning
#  ↓
# Memory Update
#  ↓
# Output

import asyncio

from cerebellum.core import CognitiveAgent
from cerebellum.runtime import CognitiveSystem

from cerebellum.perception import TextPerception
from cerebellum.controller import SimpleController

from cerebellum.memory import WorkingMemory
from cerebellum.memory import EpisodicMemory
from cerebellum.memory import SemanticMemory
from cerebellum.memory import MemoryStream

from cerebellum.planners import SimplePlanner

from cerebellum.reasoning import HierarchicalReasoner
from cerebellum.reasoning import LLMReasoner

from cerebellum.tools import WebSearchTool
from cerebellum.tools import DatabaseTool

from cerebellum.observability import Tracer
from cerebellum.observability import Metrics


async def main():

    # -----------------------------
    # Observability
    # -----------------------------

    tracer = Tracer()
    metrics = Metrics()

    # -----------------------------
    # Perception
    # -----------------------------

    perception = TextPerception()

    # -----------------------------
    # Memory System
    # -----------------------------

    working_memory = WorkingMemory()
    episodic_memory = EpisodicMemory()
    semantic_memory = SemanticMemory()
    memory_stream = MemoryStream()

    memory_system = {
        "working": working_memory,
        "episodic": episodic_memory,
        "semantic": semantic_memory,
        "stream": memory_stream,
    }

    # -----------------------------
    # Tools
    # -----------------------------

    web_search = WebSearchTool()
    database = DatabaseTool()

    tools = {
        "web_search": web_search,
        "database": database
    }

    # -----------------------------
    # Planner
    # -----------------------------

    planner = SimplePlanner()

    # -----------------------------
    # Reasoning Engine
    # -----------------------------

    worker_reasoner = LLMReasoner()

    reasoner = HierarchicalReasoner(
        planner=planner,
        worker=worker_reasoner
    )

    # -----------------------------
    # Controller
    # -----------------------------

    controller = SimpleController()

    # -----------------------------
    # Cognitive System
    # -----------------------------

    system = CognitiveSystem(
        perception=perception,
        controller=controller,
        memory=memory_system,
        planner=planner,
        reasoner=reasoner,
        tools=tools,
        tracer=tracer,
        metrics=metrics
    )

    # -----------------------------
    # Agent
    # -----------------------------

    agent = CognitiveAgent(system)

    result = await agent.run(
        "Analyze the AI market in Latin America"
    )

    print("\nFINAL RESULT\n")
    print(result)


asyncio.run(main())