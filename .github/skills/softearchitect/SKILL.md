---
name: softearchitect
description: Skill to be used to review, design, and validate cognitive architecture and event-bus interactions. Good for refactoring.
---

# Skill: Software Architecture (Cognitive Systems)

## Purpose
Use this skill when tasked with designing a new cognitive module, modifying the message bus, or restructuring the `cerebellum` data flow.

## Implementation Steps
1. **Analyze Data Flow:** Determine the incoming input and the expected output structures using the components defined in `models.py` (e.g., `Plan`, `PerceptionResult`).
2. **Design Interfaces:** Ensure any new class implements abstract methods correctly (e.g., `execute(plan, memory, tools) -> Any` for Reasoners).
3. **Identify Interactions:** Ensure communication is exclusively done via publishing and subscribing to topics on the `EventBus`.
4. **Assess Memory Integration:** Consider how the module utilizes `WorkingMemory`, `SemanticMemory`, or `EpisodicMemory`.
5. **Testability:** Structure the architectural change so it can be easily tested using `patch` and `AsyncMock` without relying on real LLM or Qdrant connections.