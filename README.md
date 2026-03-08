# Cerebellum

Cerebellum is a "Cognitive Framework" proposal for a modern cognitive architecture for AI agents — essentially the blueprint that many research labs are exploring to build systems closer to general intelligence.

The core idea: a **cognitive system** built from multiple specialized cognitive subsystems working together.

---

## Architecture Overview

```
                 USER
                   │
                   ▼
             Perception Layer
                   │
                   ▼
            Cognitive Controller
      ┌───────────┼───────────┐
      │           │           │
   Memory      Reasoning     Planning
      │           │           │
      └───────────┼───────────┘
                  │
               Tool Layer
                  │
             Environment
                  │
             Observability
```

> **Key insight:** The LLM lives *inside* the Reasoning Engine — it is not the entire system.

---

## Components

### 1. Perception Layer
Interprets the world. Processes inputs such as text, audio, images, documents, APIs, and system events, then transforms them into structured representations: intent, entities, context, and goals.

### 2. Cognitive Controller
The "executive brain" — analogous to the human prefrontal cortex. Responsible for:
- Goal tracking
- Task switching
- Agent coordination
- Reasoning orchestration

Can be implemented as an LLM, a planner, a state machine, or a policy model.

### 3. Memory System
A complete cognitive architecture requires multiple memory types:

| Type | Description | Examples |
|---|---|---|
| **Working Memory** | Temporary memory for current thought | Current task, recent reasoning steps |
| **Episodic Memory** | Records of past experiences | Conversation history, past actions |
| **Semantic Memory** | World knowledge | Facts, documents, knowledge base |
| **Procedural Memory** | Knowing how to do things | Tool usage, workflows, skills |

Typically implemented using vector DBs, graph DBs, or document stores.

### 4. Reasoning Engine
Where the LLM (or LRM — Large Reasoning Model) lives. Performs analysis, deduction, hypothesis generation, and problem solving using techniques like:
- Chain-of-thought
- Tree-of-thought
- Recursive reasoning
- HRM (Hierarchical Reasoning Model)

### 5. Planner
Decomposes complex goals into actionable subtasks using LLMs, planning algorithms, or task graphs.

### 6. Tool / Action Layer
Enables interaction with the real world: API calls, database queries, web browsing, code execution, and more. Specialized agents operate at this layer.

### 7. Learning Loop
Allows the system to learn from experience:

```
Action → Observation → Evaluation → Memory Update
```

This enables prompt improvement, workflow learning, and decision optimization.

---

## Observability
A first-class citizen in this architecture. Monitors reasoning steps, tool usage, latency, errors, and decision paths from the ground up — not as an afterthought.

---

## Motivation

Most current frameworks only cover a small fraction of a full cognitive architecture:

| Framework | Coverage |
|---|---|
| LangGraph | Agent orchestration |
| AutoGen | Multi-agent coordination |
| Semantic Kernel | Tool orchestration |

**None implement a complete cognitive architecture.** Cerebellum aims to change that.

---

## Vision

The next generation of AI systems will likely be built from the convergence of:

```
Foundation Models
+
Reasoning Models
+
Cognitive Architectures
+
Cognitive Agents (Autonomous)
```

---

## Getting Started

**Requirements:** Python >= 3.13

```bash
# Clone the repository
git clone https://github.com/Root1V/cerebellum-architecture.git
cd cerebellum

# Install dependencies
pip install -e .

# Run
python main.py
```

---

## Project Structure

```
cerebellum/
├── examples/
│   └── research_agent.py        # Example: research agent using the full system
├── src/
│   └── cerebellum/
│       ├── __init__.py
│       ├── core/                # Abstract interfaces (ABCs)
│       │   ├── agent.py         # CognitiveAgent — entry point for running tasks
│       │   ├── attention.py     # Attention — filter relevant information
│       │   ├── controller.py    # CognitiveController — orchestrates the cognitive loop
│       │   ├── learning.py      # Learning — updates from experience
│       │   ├── memory.py        # Memory — abstract store/retrieve interface
│       │   ├── perception.py    # Perception — processes raw input
│       │   ├── planner.py       # Planner — decomposes goals into steps
│       │   ├── reasoning.py     # Reasoner — executes a plan
│       │   ├── action.py        # Action — executes actions in the environment
│       │   ├── tool.py          # Tool — abstract interface for external tools
│       │   └── environment.py   # Environment — world the agent interacts with
│       ├── controller/          # Controller implementations
│       │   ├── simple_controller.py
│       │   ├── attention_manager.py
│       │   └── goal_manager.py
│       ├── memory/              # Memory implementations
│       │   ├── working_memory.py
│       │   ├── episodic_memory.py
│       │   ├── semantic_memory.py
│       │   ├── procedural_memory.py
│       │   ├── memory_stream.py
│       │   ├── vector_memory.py
│       │   └── graph_memory.py
│       ├── perception/          # Perception implementations
│       │   ├── text_perception.py
│       │   └── multimodal_perception.py
│       ├── planners/            # Planner implementations
│       │   ├── llm_planner.py
│       │   ├── simple_planner.py
│       │   └── task_graph_planner.py
│       ├── reasoning/           # Reasoning implementations
│       │   ├── llm_reasoner.py
│       │   ├── recursive_reasoner.py
│       │   ├── tree_reasoner.py
│       │   └── hrm_reasoner.py
│       ├── runtime/             # Cognitive system loop
│       │   ├── cognitive_system.py
│       │   ├── event_bus.py
│       │   └── event_loop.py
│       ├── tools/               # Tool implementations
│       │   ├── web_search.py
│       │   ├── code_executor.py
│       │   └── database_tool.py
│       └── observability/       # Tracing and metrics
│           ├── tracer.py
│           └── metrics.py
├── main.py
└── pyproject.toml
```

---

## Status

> This project is in early research and development. The architecture described here serves as the conceptual foundation for the implementation.


---
Principies:
1. Event-Driven Cognition
2. Memory Streams (tipo cerebro humano)
3. Cognitive Loop completo

Environment
     │
     ▼
Event Bus
     │
     ▼
Perception
     │
     ▼
Memory Streams
     │
     ▼
Cognitive Controller
     │
     ▼
Reasoning Loop
     │
     ▼
Tools / Actions
     │
     ▼
New Events


Las 7 interfaces cognitivas fundamentales
1. Perception
2. Attention
3. Memory
4. Reasoning
5. Planning
6. Action
7. Learning

Environment
     │
     ▼
Perception
     │
     ▼
Attention
     │
     ▼
Memory
     │
     ▼
Reasoning
     │
     ▼
Planning
     │
     ▼
Action
     │
     ▼
Learning