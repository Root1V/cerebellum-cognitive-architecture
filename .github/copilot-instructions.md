# Cerebellum - Copilot Instructions

You are assisting with **Cerebellum**, a distributed, asynchronous, event-driven cognitive architecture inspired by neuroscience. 

When generating or refactoring code for this project, you must adhere strictly to the following architectural and coding constraints:

## 1. Core Stack & Typing
- **Language**: Python 3.13+
- **Typing**: Use strict type hints for all functions, methods, and classes. The codebase must pass `mypy src` perfectly. Do not use `Any` unless absolutely necessary (e.g., dynamic event payloads).
- **Models**: Use `pydantic` (`BaseModel`) for all data structures (Thoughts, Plans, Perceptions).
- **Core Libraries**: `asyncio`, `fastapi`, `qdrant-client` (AsyncQdrantClient), `axonium` (custom LLM SDK).

## 2. Asynchronous Programming (Async-First)
- All I/O bound operations (database calls, LLM generation, API requests, Event Bus publishing) **must be asynchronous** (`async def` and `await`).
- Never use blocking synchronous code (no `requests`, no sync `time.sleep`).

## 3. Event-Driven Architecture (The Golden Rule)
- **Zero Direct Coupling**: Cognitive modules (`Perception`, `Memory`, `Reasoning`, `Planning`, `Action`) must **never** call each other's methods directly.
- **Event Bus Only**: All cross-module communication happens strictly by publishing and subscribing to topics via the `EventBus`.
- Always structure module architectures anticipating they will react to incoming `dict` or `pydantic` payloads from the bus, and emit results back to the bus.

## 4. Testing & Mocks
- Use `pytest` for all tests.
- Use `@pytest.mark.asyncio` for asynchronous tests.
- **Isolate tests**: Do NOT hit real external services (Qdrant, LLM servers) during unit tests. Always use `unittest.mock.patch` or `AsyncMock` to mock `EpisodicMemory` retrievals or `Axonium` LLM calls.

## 5. Clean Code & Conventions
- **No Print Statements**: Use Python's built-in `logging` module (`logger = logging.getLogger("cerebellum.module")`) for observability.
- **Small Modules**: Keep classes and functions small and composable following SOLID principles.
- Format code elegantly, avoiding deep nesting where possible.