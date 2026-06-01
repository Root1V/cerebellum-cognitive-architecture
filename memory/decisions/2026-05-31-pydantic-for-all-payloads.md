# Decision: Pydantic BaseModel for All Cross-Module Payloads

**Date:** 2026-05-31  
**Status:** Accepted  

---

## Context

Cognitive modules communicate via the EventBus by passing data payloads. Without a schema contract, raw `dict` payloads can silently drop fields, carry incorrect types, and make refactoring unsafe.

## Decision

All event bus payloads and data structures passed between cognitive modules MUST be `pydantic.BaseModel` subclasses. These models are defined in `src/cerebellum/cognition/runtime/protocols.py` and `src/cerebellum/cognition/core/models.py`.

Specifically:
- No `dict`, `Any`, or untyped tuples may cross a module boundary.
- New payload types MUST be added to `protocols.py` before any module uses them.
- Existing models MUST NOT have fields removed without a spec change.

## Rationale

- Pydantic provides runtime validation, clear field definitions, and IDE autocompletion.
- A shared `protocols.py` acts as the API contract between modules.
- Breaking changes to models are immediately visible at deserialization time.
- mypy + pydantic catches type errors at development time, not at runtime.

## Consequences

- Every new inter-module event requires a new `pydantic.BaseModel` in `protocols.py`.
- `mypy src` must pass with 0 errors — `Any` is forbidden except at external JSON boundaries.
- When receiving raw LLM output or external API responses, always coerce to a `pydantic` model within the infrastructure boundary before passing to cognition.

## Rejected Alternatives

- **Raw dict**: no validation, no IDE support, silent bugs.
- **dataclasses**: no runtime validation, harder to integrate with FastAPI and JSON.
- **TypedDict**: no runtime validation.

## References

- `src/cerebellum/cognition/runtime/protocols.py`
- `src/cerebellum/cognition/core/models.py`
- `.github/instructions/coding.instructions.md` — Rule 3: Data Integrity with Pydantic
