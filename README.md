# Cerebellum

Cerebellum is a proposal for a modern cognitive architecture for AI agents — essentially the blueprint that many research labs are exploring to build systems closer to general intelligence.

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
git clone https://github.com/your-username/cerebellum.git
cd cerebellum

# Install dependencies
pip install -e .

# Run
python main.py
```

---

## Status

> This project is in early research and development. The architecture described here serves as the conceptual foundation for the implementation.
