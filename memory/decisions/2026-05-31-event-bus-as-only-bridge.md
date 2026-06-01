# Decision: Event Bus as the Only Bridge Between Cognitive Modules

**Date:** 2026-05-31  
**Status:** Accepted  

---

## Context

Cerebellum is built as a collection of specialised cognitive modules (Perception, Attention, Memory, Reasoning, Action, Learning). A naive implementation would have these modules hold references to each other, creating tight coupling that makes testing, swapping, and extending individual modules difficult.

## Decision

All cross-module communication flows exclusively through the `EventBus` (`src/cerebellum/cognition/runtime/event_bus.py`). No cognitive module may directly instantiate, import, or call methods on a sibling cognitive module.

Modules interact only by:
1. **Subscribing** to topics (e.g. `perception.output`)
2. **Publishing** to topics (e.g. `memory.store`)

The `CognitiveRuntime` is the only entity allowed to wire modules together at startup.

## Rationale

- **Testability**: each module can be unit-tested in isolation by publishing directly to the bus with mocked data.
- **Replaceability**: any module can be swapped for a different implementation without touching sibling modules.
- **Observability**: all cognitive events flow through one point, making tracing and logging straightforward.
- **Extensibility**: new modules subscribe to existing topics without modifying existing code.

## Consequences

- Every new cognitive module MUST inherit from `CognitiveModule` and register via `CognitiveRuntime`.
- All event payloads MUST use `pydantic` models defined in `src/cerebellum/cognition/runtime/protocols.py`.
- Topic names MUST follow the `<domain>.<action>` convention (lowercase, dot-separated).
- Direct imports of sibling cognitive modules (outside `core/` and `runtime/`) are forbidden.

## Rejected Alternatives

- **Direct method calls**: simple but creates tight coupling and makes module isolation impossible.
- **Dependency injection via constructor**: reduces coupling but still requires modules to know each other's interfaces at construction time.

## References

- `src/cerebellum/cognition/runtime/event_bus.py`
- `src/cerebellum/cognition/runtime/cognitive_runtime.py`
- `src/cerebellum/cognition/runtime/protocols.py`
- `.github/instructions/architecture.instructions.md`
