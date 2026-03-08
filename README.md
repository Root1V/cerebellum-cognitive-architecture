# Cerebellum

A cognitive architecture framework for building AI agents — not just LLM wrappers, but systems with memory, planning, reasoning, and learning working together as a unified cognitive loop.

The core idea: a **cognitive system** built from multiple specialized subsystems, where the LLM is one component of the reasoning engine, not the entire system.

---

## Architecture - Level 0: Cognitive
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


## C4 Architecture — Level 1: System Context

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          C4 — SYSTEM CONTEXT                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

          ┌─────────────────────┐
          │      Developer /    │
          │    Application      │   Sends tasks, receives results.
          │    [Person/System]  │   Uses cerebellum as a library
          └──────────┬──────────┘
                     │  agent.run("task")
                     ▼
          ┌──────────────────────────────────────────┐
          │                                          │
          │           CEREBELLUM                     │
          │      Cognitive Architecture              │
          │                                          │
          │  A framework for building cognitive AI   │
          │  agents with full perception → memory    │
          │  → planning → reasoning → action loop.   │
          │                                          │
          │  [Python library — cerebellum-arch]      │
          │                                          │
          └───┬──────────────┬──────────────┬────────┘
              │              │              │
              ▼              ▼              ▼
  ┌───────────────┐  ┌──────────────┐  ┌───────────────────┐
  │  Local LLM    │  │ External     │  │  World /          │
  │  Server       │  │ Tools        │  │  Environment      │
  │               │  │              │  │                   │
  │ LM Studio,    │  │ Web search,  │  │ APIs, databases,  │
  │ Ollama,       │  │ databases,   │  │ file systems,     │
  │ llama.cpp,    │  │ APIs,        │  │ knowledge bases,  │
  │ OpenAI API    │  │ code exec.   │  │ system prompts    │
  │ [HTTP/REST]   │  │ [API calls]  │  │ [any source]      │
  └───────────────┘  └──────────────┘  └───────────────────┘
```

---

## C4 Architecture — Level 2: Containers

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          C4 — CONTAINERS                                     ║
║               (packages inside the cerebellum library)                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Developer
      │
      │  agent.run("Analyze AI market in LATAM")
      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          cerebellum library                             │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      CognitiveAgent                              │   │
│  │               [core/agent.py — entry point]                      │   │
│  │   Accepts a task string. Delegates to CognitiveSystem.run().     │   │
│  └───────────────────────────────┬──────────────────────────────────┘   │
│                                  │                                      │
│                                  ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                     CognitiveSystem                              │   │
│  │              [runtime/cognitive_system.py — orchestrator]        │   │
│  │                                                                  │   │
│  │  Runs the full cognitive loop in 9 steps:                        │   │
│  │  0. Environment.observe()  →  world state                        │   │
│  │  1. Perception.perceive()  →  structured input                   │   │
│  │  2. Attention.select()     →  focused context                    │   │
│  │  3. Controller.interpret() →  goal                               │   │
│  │  4. Memory.recall()        →  past context                       │   │
│  │  5. Planner.create_plan()  →  steps                              │   │
│  │  6. Reasoner.execute()     →  result                             │   │
│  │  6.5 Action.execute()      →  environmental effect               │   │
│  │  7. Learning.update()      →  experience stored                  │   │
│  │  8. Memory.store_event()   →  episodic update                    │   │
│  │  9. Controller.is_goal_satisfied() → recurse or return           │   │
│  └──┬────────┬──────────┬──────────┬──────────┬──────────┬──────────┘   │
│     │        │          │          │          │          │              │
│     ▼        ▼          ▼          ▼          ▼          ▼              │
│  ┌──────┐ ┌──────┐ ┌────────┐ ┌────────┐ ┌───────┐ ┌─────────────┐      │
│  │ Per- │ │Atten-│ │Control-│ │Memory  │ │Planner│ │  Reasoner   │      │
│  │ cep- │ │tion  │ │  ler   │ │System  │ │       │ │  (ReAct     │      │
│  │ tion │ │      │ │        │ │        │ │Simple-│ │   Loop)     │      │
│  │      │ │Simp- │ │Simple- │ │Working │ │Planner│ │             │.     │ 
│  │Text- │ │leAt- │ │Control-│ │Episodic│ │LLM-   │ │LoopReasoner │      │
│  │Perc- │ │ten-  │ │  ler   │ │Semantic│ │Planner│ │LLMReasoner  │      │
│  │tion  │ │tion  │ │        │ │Proced- │ │Task-  │ │HierarchReas-│      │
│  │Multi-│ │      │ │Goal-   │ │ural    │ │Graph- │ │oner         │      │ 
│  │modal │ │      │ │Manager │ │Vector  │ │Planner│ │Recursive-   │      │
│  │      │ │      │ │Attn-   │ │Graph   │ │       │ │Reasoner     │      │
│  │      │ │      │ │Manager │ │Stream  │ │       │ │             │      │
│  └──────┘ └──────┘ └────────┘ └────────┘ └───────┘ └──────┬──────┘      │
│                                                           │             │
│  ┌─────────────┐   ┌─────────────┐   ┌────────────────┐   │             │
│  │   Action    │   │ Environment │   │  Observability │   │             │
│  │             │   │             │   │                │   │             │
│  │ConsoleAction│   │TextEnvironm.│   │ Tracer         │   │             │
│  │             │   │SystemPrompt │   │ Metrics        │   │             │
│  │  Produces   │   │KnowledgeBase│   │                │   │             │
│  │ env effects │   │APIEnvironm. │   │ Traces every   │   │             │
│  │ after reason│   │             │   │ step of the    │   │             │
│  └─────────────┘   └─────────────┘   │ cognitive loop │   │             │
│                                      └────────────────┘   │             │
│  ┌────────────────────────────────────────────────────────▼─────────┐   │
│  │                    LLM Adapter                                   │   │
│  │                  [llm/llama_adapter.py]                          │   │
│  │                                                                  │   │
│  │  Wraps axonium SDK. Exposes complete(prompt) and chat(messages). │   │
│  │  Used by LLMPlanner and LLMReasoner as llm_client.               │   │
│  └───────────────────────────────┬──────────────────────────────────┘   │
│                                  │                                      │
└──────────────────────────────────┼──────────────────────────────────────┘
                                   │  HTTP / REST
                                   ▼
                       ┌───────────────────────┐
                       │   Local LLM Server    │
                       │  (Ollama, LM Studio,  │
                       │   llama.cpp, OpenAI)  │
                       └───────────────────────┘
```

> **Key insight:** The LLM lives *inside* the Reasoning Engine and the Planner — it is a component, not the entire system.

---

## Cognitive Loop — Step by Step

```
  Task input
      │
      ▼
  ┌─────────────────────────────────────────────────┐
  │  Step 0   Environment.observe()                 │  ← world state enriches all
  │  Step 1   Perception.perceive(input)            │  ← raw → structured
  │  Step 2   Attention.select(perception, memory)  │  ← filter relevance
  │  Step 3   Controller.interpret(focused)         │  ← set goal
  │  Step 4   Memory.recall(goal)                   │  ← past context
  │  Step 5   Planner.create_plan(goal, context)    │  ← decompose
  │  Step 6   Reasoner.execute(plan, memory, tools) │  ← think (ReAct loop)
  │  Step 6.5 Action.execute(result)                │  ← act in the world
  │  Step 7   Learning.update(experience)           │  ← learn
  │  Step 8   Memory.store_event(...)               │  ← remember
  │  Step 9   Controller.is_goal_satisfied()?       │  ── no ──▶ recurse
  └─────────────────────────────────────────────────┘       │
                                                           yes
                                                             ▼
                                                         return result
```

---

## Components

### Perception
Processes raw input (text, multimodal) into structured `{"content", "intent", "context"}`.

### Attention
Filters what is relevant from perception + memory. Only focused context reaches planning.

### Cognitive Controller
The executive layer — translates perception into a goal (`interpret`), evaluates if the goal was met (`is_goal_satisfied`), and generates sub-goals if not (`next_goal`). Analogous to the prefrontal cortex.

### Memory System

| Type | Class | Role |
|---|---|---|
| Working | `WorkingMemory` | Current reasoning context |
| Episodic | `EpisodicMemory` | Past experiences and events |
| Semantic | `SemanticMemory` | World knowledge / facts |
| Procedural | `ProceduralMemory` | How-to knowledge / skills |
| Vector | `VectorMemory` | Similarity search |
| Graph | `GraphMemory` | Relational knowledge |
| Stream | `MemoryStream` | Temporal event stream |

### Planner
Decomposes goals into ordered steps. `SimplePlanner` derives step names directly from registered tools — tool names become the plan, no domain knowledge hardcoded.

### Reasoning Engine
Implements various reasoning strategies over a plan:

| Class | Strategy |
|---|---|
| `LoopReasoner` | ReAct — think → invoke → evaluate loop |
| `LLMReasoner` | Sequential LLM delegation per step |
| `HierarchicalReasoner` | Hierarchical planning + worker decomposition |
| `RecursiveReasoner` | Recursive sub-problem decomposition |

### Action
Produces **environmental effects** after reasoning — prints, writes, calls APIs. Distinct from tool invocation inside the reasoning loop.

### Environment
World context observable by the agent. Four implementations:

| Class | Use case |
|---|---|
| `TextEnvironment` | Plain text context string |
| `SystemPromptEnvironment` | LLM system prompt + constraints |
| `KnowledgeBaseEnvironment` | Document store / RAG |
| `APIEnvironment` | External API state (override `_fetch()`) |

### LLM Adapter
Wraps local LLM servers via the `axonium` SDK. Exposes `complete(prompt)` and `chat(messages)` used by `LLMPlanner` and `LLMReasoner`.

### Observability
`Tracer` and `Metrics` are first-class citizens — wired into `CognitiveSystem` and active at every step of the loop.

---

## Motivation

Most current frameworks cover only a fraction of a full cognitive architecture:

| Framework | Coverage |
|---|---|
| LangGraph | Agent orchestration |
| AutoGen | Multi-agent coordination |
| Semantic Kernel | Tool orchestration |

**None implement a complete cognitive loop.** Cerebellum aims to change that.

---

## Vision

The next generation of AI systems converges:

```
Foundation Models  +  Reasoning Models  +  Cognitive Architectures  +  Autonomous Agents
```

---

## Getting Started

**Requirements:** Python >= 3.13

```bash
# Clone
git clone https://github.com/Root1V/cerebellum-architecture.git
cd cerebellum

# Install
pip install -e .

# Run basic example
python examples/research_basic.py

# Run full agent example
python examples/research_agent.py

# Run with local LLM (requires LLM_BASE_URL env var)
LLM_BASE_URL=http://localhost:8080 python examples/llama_cerebellum_example.py
```

---

## Project Structure

```
cerebellum/
├── examples/
│   ├── research_basic.py              # Minimal cognitive loop
│   ├── research_agent.py              # Full agent with tools + observability
│   └── llama_cerebellum_example.py    # Local LLM via axonium SDK
├── src/
│   └── cerebellum/
│       ├── core/                      # Abstract interfaces (ABCs)
│       │   ├── agent.py               # CognitiveAgent
│       │   ├── controller.py          # CognitiveController
│       │   ├── perception.py          # Perception
│       │   ├── attention.py           # Attention
│       │   ├── memory.py              # Memory
│       │   ├── planner.py             # Planner
│       │   ├── reasoning.py           # Reasoner
│       │   ├── action.py              # Action
│       │   ├── tool.py                # Tool
│       │   ├── environment.py         # Environment
│       │   └── learning.py            # Learning
│       ├── runtime/                   # Orchestration only
│       │   └── cognitive_system.py    # 9-step cognitive loop
│       ├── controller/                # Controller implementations
│       ├── perception/                # Perception implementations
│       ├── attention/                 # Attention implementations
│       ├── memory/                    # 7 memory types
│       ├── planners/                  # SimplePlanner, LLMPlanner, TaskGraphPlanner
│       ├── reasoning/                 # LoopReasoner, LLMReasoner, HRM, Recursive
│       ├── action/                    # ConsoleAction
│       ├── environment/               # 4 environment types
│       ├── tools/                     # WebSearchTool, DatabaseTool, CodeExecutor
│       ├── llm/                       # LlamaAdapter (axonium SDK)
│       ├── learning/                  # SimpleLearning
│       └── observability/             # Tracer, Metrics
├── main.py
└── pyproject.toml
```

---

## Status

Early development. The architecture is functional end-to-end. LLM integration requires a local server (Ollama, LM Studio, llama.cpp) or compatible API.

**Design principles:**
1. Each core ABC has its own implementation package — no logic in `runtime/`
2. `runtime/` is orchestration only — `CognitiveSystem` wires the loop
3. The Planner decides *what* steps to run; the Reasoner decides *how* to execute them
4. Tool names are the plan — `SimplePlanner` derives steps from registered tools directly
