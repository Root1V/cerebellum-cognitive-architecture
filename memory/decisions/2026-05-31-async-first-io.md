# Decision: Async-First I/O — No Synchronous Blocking Calls

**Date:** 2026-05-31  
**Status:** Accepted  

---

## Context

Cerebellum processes cognitive loops that involve multiple concurrent I/O operations: LLM inference, vector database queries, tool calls, and memory retrieval. Blocking any of these on a synchronous thread would stall the entire cognitive loop.

## Decision

All I/O-bound operations in Cerebellum MUST be implemented as `async def` functions using `await`. The following are explicitly forbidden:

- `requests` (use `httpx.AsyncClient`)
- `time.sleep` (use `asyncio.sleep`)
- Synchronous Qdrant client (use `qdrant_client.AsyncQdrantClient`)
- Any synchronous LLM call (use `axonium` async interface)

## Rationale

- Python's `asyncio` event loop enables high concurrency within a single process.
- The cognitive loop can overlap memory recall, LLM inference, and tool calls without thread management overhead.
- `pytest-asyncio` and `AsyncMock` provide first-class async testing support with no extra complexity.

## Consequences

- Every new function touching the network, filesystem, or external services must be `async def`.
- Tests for such functions must use `@pytest.mark.asyncio`.
- All external dependencies must have an async-compatible API.

## Rejected Alternatives

- **Threading**: adds complexity, GIL contention, and harder-to-reason concurrency.
- **Sync-first with async wrapper**: masks blocking operations and defeats the purpose.

## References

- `pyproject.toml` — `asyncio`, `qdrant-client`, `axonium`, `httpx`
- `.github/instructions/coding.instructions.md` — Rule 1: Async-First
