---
id: "001"
title: "Fix Blocking I/O in EmbeddingClient"
status: closed
current-agent: release-agent
created: 2026-05-31T20:00:00Z
updated: 2026-06-01T00:39:39Z
pipeline-log:
  - agent: spec-writer-agent
    status: draft
    timestamp: 2026-05-31T20:00:00Z
  - agent: developer-agent
    status: implementing
    timestamp: 2026-06-01T00:21:35Z
  - agent: developer-agent
    status: code-complete
    timestamp: 2026-06-01T00:21:35Z
  - agent: test-agent
    status: testing
    timestamp: 2026-06-01T00:22:36Z
  - agent: test-agent
    status: tests-passed
    timestamp: 2026-06-01T00:24:18Z
  - agent: security-reviewer-agent
    status: reviewing
    timestamp: 2026-06-01T00:26:18Z
  - agent: security-reviewer-agent
    status: security-approved
    timestamp: 2026-06-01T00:26:25Z
  - agent: docs-agent
    status: documenting
    timestamp: 2026-06-01T00:28:05Z
  - agent: docs-agent
    status: implemented
    timestamp: 2026-06-01T00:28:05Z
  - agent: release-agent
    status: closed
    timestamp: 2026-06-01T00:37:46Z

# 001 — Fix Blocking I/O in EmbeddingClient

## Problem Statement

`EmbeddingClient.encode()` in `src/cerebellum/infraestructure/llm/embedd_client.py` calls `self._model.encode()` (a `sentence-transformers` CPU-bound operation) synchronously inside an `async def` method. This directly blocks the `asyncio` event loop for the duration of the encoding operation — typically 50–500 ms depending on hardware and text length.

**Who is affected:** Every component that uses `EmbeddingClient`:
- `SimpleAttentionModule` — blocks on `on_start()` and on every `attention.set_focus` message
- `EpisodicMemory` — blocks on every `memory.store` (episodic) and `memory.search` call

**Impact if not fixed:** The cognitive loop stalls on every embedding operation. All other modules waiting for messages — reasoning, action, learning — are frozen during this time. This is the single most critical correctness issue in the current codebase.

## Goals

- [ ] Offload `SentenceTransformer.encode()` to a thread pool so the event loop is never blocked
- [ ] Maintain the existing `Embedding` ABC contract without changing its signature
- [ ] Verify that attention focus initialization and episodic memory operations are non-blocking

## Non-Goals

- Not changing the embedding model (`all-MiniLM-L6-v2`)
- Not changing the `Embedding` ABC or any caller interface
- Not adding model caching or warm-up logic (separate concern)
- Not changing `SimpleAttentionModule` or `EpisodicMemory` — the fix is isolated to the infra layer

## Proposed Solution

Replace the synchronous call with `asyncio.to_thread()`, which schedules the CPU-bound function on the default `ThreadPoolExecutor` and `await`s its completion without blocking the event loop.

**Before:**
```python
async def encode(self, text: str | None = None) -> Any:
    vectors = self._model.encode(text or "")   # ← blocks event loop
    return vectors.tolist()
```

**After:**
```python
import asyncio

async def encode(self, text: str | None = None) -> Any:
    vectors = await asyncio.to_thread(self._model.encode, text or "")
    return vectors.tolist()
```

`asyncio.to_thread()` is the standard Python 3.9+ primitive for this pattern. It is available in Python 3.13 (which this project requires).

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Use `asyncio.to_thread()` over `loop.run_in_executor()` | `to_thread` is the modern, high-level API for this pattern in Python 3.9+; no need to acquire a loop reference manually |
| Fix only `embedd_client.py`, not the ABC | The `Embedding` ABC already declares `encode` as `async def` — the contract is correct, only the implementation is wrong |
| No thread pool configuration | Default `ThreadPoolExecutor` is appropriate for infrequent encoding calls; pool sizing is a separate operational concern |

## API Contract

No API contract changes. `encode()` signature and return type remain identical.

## Data Model

No data model changes.

## Security Considerations

- No secrets or credentials involved.
- No user input reaches `self._model.encode()` without passing through `PerceptionProcessPayload` pydantic validation first. No injection risk introduced by this change.
- Thread pool execution does not share mutable state between concurrent calls (each call receives its own `text` argument and the underlying `SentenceTransformer` model is thread-safe for inference).

## Acceptance Criteria

- [x] AC-1: Given `EmbeddingClient.encode("test text")` is called from an async context, when the call is awaited, then the event loop is not blocked (other coroutines can run concurrently during encoding).
- [x] AC-2: Given `SimpleAttentionModule.on_start()` is called, when it initializes the focus vector, then it completes without blocking the event loop and sets `_focus_vector` to a non-empty list.
- [x] AC-3: Given `SimpleAttentionModule` receives an `attention.set_focus` message, when `encode()` is called for the new focus query, then the event loop remains free and `_focus_vector` is updated correctly.
- [x] AC-4: Given `EpisodicMemory` receives a `memory.store` message with `scope: episodic`, when it generates the embedding for storage, then the encoding is non-blocking and the vector is stored in Qdrant.
- [x] AC-5: Given `EpisodicMemory` receives a `memory.search` message, when it generates the query embedding, then the encoding is non-blocking and results are returned.
- [x] AC-6: Given the fix is applied, when `uv run mypy src` is executed, then it exits with 0 errors.
- [x] AC-7: Given the fix is applied, when `uv run ruff check .` is executed, then it exits with 0 warnings.

## E2E Validation

> Script: `validations/001-fix-blocking-io-embedding-client.py`
> Run against a live runtime (no Qdrant required — mock storage) to confirm concurrent coroutine execution during embedding calls.

## Open Questions

- None
