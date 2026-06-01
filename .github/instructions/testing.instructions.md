---
description: "Testing conventions for the Cerebellum cognitive architecture. Covers pytest-asyncio setup, mock strategy, test naming, file organisation, and how to run the full validation suite."
applyTo: "tests/**"
---

# Testing Instructions — Cerebellum

## 1. Test Framework

- **Runner:** `pytest` with `pytest-asyncio`
- **Run all tests:** `uv run pytest tests/ -v`
- **Run a single suite:** `uv run pytest tests/unit/ -v`
- **Run type check:** `uv run mypy src`
- **Run linter:** `uv run ruff check .`

All checks must pass before handing off to the next SDD pipeline stage.

## 2. Async Tests (MANDATORY)

Every test that touches async code MUST use `@pytest.mark.asyncio`.

```python
import pytest

@pytest.mark.asyncio
async def test_perception_process_AC1():  # memory/specs/001-perception.md — AC-1
    result = await perception.process("raw input")
    assert result.intent == "search"
```

Never use `asyncio.run()` inside tests. Never write synchronous wrappers around async functions.

## 3. Mocking External Dependencies

**Rule: Never hit real external services during unit tests.**

Always mock:
- `axonium` / LLM calls → `AsyncMock`
- `qdrant-client` / `AsyncQdrantClient` calls → `AsyncMock`
- Any `httpx` / network calls → `AsyncMock`

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_episodic_memory_recall_AC2():  # memory/specs/002-episodic-memory.md — AC-2
    with patch(
        "cerebellum.infraestructure.storage.db_episodic.AsyncQdrantClient.search",
        new_callable=AsyncMock,
    ) as mock_search:
        mock_search.return_value = []
        result = await episodic_memory.recall("context query")
        assert result == []
```

## 4. Test Naming Convention

```
test_<short_description>_AC<N>
```

Every test function MUST include a comment on the same line or the next line referencing the spec:

```python
def test_event_published_on_perception_output_AC3():  # memory/specs/003-event-bus.md — AC-3
    ...
```

## 5. File Organisation

```
tests/
├── unit/                  # Pure unit tests — no real I/O, all mocked
│   └── test_cognition.py  # Cognitive module unit tests
├── integration/           # Integration tests — may use in-process components
│   ├── test_llm_integration.py
│   └── test_storage_integration.py
└── agent_eval/            # Agent-level evaluation scenarios
    ├── test_memory.py
    ├── test_planning.py
    └── test_reasoning.py
```

- Unit tests go in `tests/unit/`.
- Integration tests (e.g. Qdrant in-process) go in `tests/integration/`.
- Agent behaviour evaluation goes in `tests/agent_eval/`.

## 6. AC Coverage Requirement

Every AC in a spec must map to at least one test function.

Minimum per AC:
- One **happy-path** test
- One **edge-case or failure** test if the AC describes error handling

## 7. Pydantic Model Validation in Tests

When testing event payloads or cognitive data structures, always construct them via the `pydantic` model — never with raw `dict`.

```python
from cerebellum.cognition.runtime.protocols import PerceptionPayload

payload = PerceptionPayload(content="raw input", intent="search", context={})
assert payload.intent == "search"
```

## 8. Event Bus Testing

When testing modules that publish or subscribe to the event bus:
- Instantiate a real `EventBus` (it is in-process with no I/O)
- Mock the downstream subscriber's `on_message` or the external calls it makes

```python
from cerebellum.cognition.runtime.event_bus import EventBus

@pytest.mark.asyncio
async def test_perception_publishes_output_AC1():  # memory/specs/001-perception.md — AC-1
    bus = EventBus()
    received = []
    bus.subscribe("perception.output", lambda msg: received.append(msg))
    await perception_module.on_message(bus, PerceptionPayload(...))
    assert len(received) == 1
```

## 9. Forbidden in Tests

- `print()` — use `caplog` fixture or `logging` if you need to assert log output
- `time.sleep()` — use `asyncio.sleep()` only when strictly necessary
- Real network calls to LLM servers or Qdrant
- Hardcoded API keys or credentials
- Modifying global state without teardown
