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

from cerebellum.action import ConsoleAction
from cerebellum.attention import SimpleAttention
from cerebellum.core import CognitiveAgent
from cerebellum.learning import SimpleLearning
from cerebellum.runtime import CognitiveSystem

from cerebellum.perception import TextPerception
from cerebellum.controller import SimpleController

from cerebellum.memory import WorkingMemory
from cerebellum.memory import EpisodicMemory
from cerebellum.memory import SemanticMemory
from cerebellum.memory import MemoryStream

from cerebellum.planners import SimplePlanner

from cerebellum.reasoning import LoopReasoner

from cerebellum.environment import TextEnvironment
from cerebellum.tools import WebSearchTool
from cerebellum.tools import DatabaseTool

from cerebellum.observability import Tracer
from cerebellum.observability import Metrics


TASK = "Analyze the AI market in Latin America"
# The environment represents the world/domain context the agent operates in,
# not the task itself. The task is what the agent is asked to do.
ENVIRONMENT_CONTEXT = "Domain: Latin American technology market. Year: 2026. Focus areas: AI, fintech, healthcare."


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

    reasoner = LoopReasoner(max_iterations=10)

    # -----------------------------
    # Controller
    # -----------------------------

    controller = SimpleController()

    # -----------------------------
    # Cognitive System
    # -----------------------------
    
    attention = SimpleAttention()
    action = ConsoleAction()
    learning = SimpleLearning()
    environment = TextEnvironment(ENVIRONMENT_CONTEXT)
    
    system = CognitiveSystem(
        perception=perception,
        attention=attention,
        memory=memory_system,
        planner=planner,
        reasoner=reasoner,
        action=action,
        learning=learning,
        environment=environment,
        controller=controller,
        tools=tools,
        tracer=tracer,
        metrics=metrics,
    )

    # -----------------------------
    # Agent
    # -----------------------------

    agent = CognitiveAgent(system)

    result = await agent.run(TASK)

    print("\nFINAL RESULT\n")
    print(result)


asyncio.run(main())


# [TRACE] input_received: Analyze the AI market in Latin America
# [ACTION] {'iteration': 1, 'action': {'step': 'search_market_data', 'meta': {'step': 1, 'action': 'search_market_data', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'Search results for AI market Latin America'}
# [ACTION] {'iteration': 2, 'action': {'step': 'analyze_trends', 'meta': {'step': 2, 'action': 'analyze_trends', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI adoption growing in fintech and healthcare'}
# [ACTION] {'iteration': 3, 'action': {'step': 'generate_summary', 'meta': {'step': 3, 'action': 'generate_summary', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI market in LATAM shows strong growth potential'}
# Environment received: [{'iteration': 1, 'action': {'step': 'search_market_data', 'meta': {'step': 1, 'action': 'search_market_data', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'Search results for AI market Latin America'}, {'iteration': 2, 'action': {'step': 'analyze_trends', 'meta': {'step': 2, 'action': 'analyze_trends', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI adoption growing in fintech and healthcare'}, {'iteration': 3, 'action': {'step': 'generate_summary', 'meta': {'step': 3, 'action': 'generate_summary', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI market in LATAM shows strong growth potential'}]
# [TRACE] action_executed: [{'iteration': 1, 'action': {'step': 'search_market_data', 'meta': {'step': 1, 'action': 'search_market_data', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'Search results for AI market Latin America'}, {'iteration': 2, 'action': {'step': 'analyze_trends', 'meta': {'step': 2, 'action': 'analyze_trends', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI adoption growing in fintech and healthcare'}, {'iteration': 3, 'action': {'step': 'generate_summary', 'meta': {'step': 3, 'action': 'generate_summary', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI market in LATAM shows strong growth potential'}]

# FINAL RESULT

# [{'iteration': 1, 'action': {'step': 'search_market_data', 'meta': {'step': 1, 'action': 'search_market_data', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'Search results for AI market Latin America'}, {'iteration': 2, 'action': {'step': 'analyze_trends', 'meta': {'step': 2, 'action': 'analyze_trends', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI adoption growing in fintech and healthcare'}, {'iteration': 3, 'action': {'step': 'generate_summary', 'meta': {'step': 3, 'action': 'generate_summary', 'goal': {'goal': 'Analyze the AI market in Latin America', 'intent': 'analyze', 'context': {}}}}, 'result': 'AI market in LATAM shows strong growth potential'}]