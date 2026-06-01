# Architecture — Cerebellum

## Cognitive Loop (9 Steps)

```
Task input
    │
    ▼
Step 0  Environment.observe()                → world state enriches all
Step 1  Perception.perceive(input)           → raw → structured PerceptionResult
Step 2  Attention.select(perception, memory) → focused context
Step 3  Controller.interpret(focused)        → set goal
Step 4  Memory.recall(goal)                  → past context
Step 5  Planner.create_plan(goal, context)   → ordered steps (Plan)
Step 6  Reasoner.execute(plan, memory, tools)→ think (ReAct loop)
Step 6.5 Action.execute(result)              → act in the world
Step 7  Learning.update(experience)          → learn
Step 8  Memory.store_event(...)              → episodic update
Step 9  Controller.is_goal_satisfied()?      → recurse or return result
```

## Module Responsibilities

| Module | Source | Listens | Emits |
|--------|--------|---------|-------|
| Perception | `cognition/perception/` | `perception.process` | `perception.output` |
| Attention | `cognition/attention/` | `perception.output`, `attention.set_focus` | `attention.focused` |
| Memory | `cognition/memory/` | `memory.[store\|recall\|search]` | `memory.[available\|stored]` |
| Planners | `cognition/planners/` | (called by Reasoner) | `reasoning.plan_ready` |
| Neural/Reasoning | `cognition/neural/` | `attention.focused` | `reasoning.plan_ready` |
| Action | `cognition/action/` | `reasoning.plan_ready` | `action.completed` |
| Learning | `cognition/learning/` | `action.completed` | (internal update) |
| CognitiveRuntime | `cognition/runtime/` | orchestrates all | — |

## Key Design Decisions

1. **No direct coupling** — cognitive modules never call each other; the EventBus is the only bridge.
2. **LLM is a component** — LLM lives inside Planners and Reasoning, not as the entire system.
3. **Infrastructure isolation** — cognition modules never import qdrant, httpx, or axonium directly.
4. **Async throughout** — every I/O bound operation is `async/await`; no blocking calls.
5. **Pydantic everywhere** — all payloads and data structures use `pydantic.BaseModel`.
