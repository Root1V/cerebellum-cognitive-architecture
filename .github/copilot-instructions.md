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

## 3. Event-Driven Choreography (The Golden Rule)
- **Zero Direct Coupling**: Cognitive modules (`Perception`, `Memory`, `Reasoning`, `Action`) must **never** call each other's methods directly.
- **CognitiveRuntime & MessageBus**: Every module must inherit from `CognitiveModule` and register itself in the `CognitiveRuntime`.
- **Core Pattern**: Modules subscribe to topics (e.g., `memory.store`, `perception.text`) and react via `on_message`. Results are emitted back to the bus via `self.publish`.
- **Choreography**: Avoid central managers or orchestrators. Successive module reactions define the flow of thought until the system reaches an idle state (`run_until_idle`).

## 4. Testing & Mocks
- Use `pytest` for all tests.
- Use `@pytest.mark.asyncio` for asynchronous tests.
- **Isolate tests**: Do NOT hit real external services (Qdrant, LLM servers) during unit tests. Always use `unittest.mock.patch` or `AsyncMock` to mock `EpisodicMemory` retrievals or `Axonium` LLM calls.

## 5. Clean Code & Conventions
- **No Print Statements**: Use Python's built-in `logging` module (`logger = logging.getLogger("cerebellum.module")`) for observability.
- **Small Modules**: Keep classes and functions small and composable following SOLID principles.
- Format code elegantly, avoiding deep nesting where possible.

## 6. Development Workflow & Branching
- **Base Branch**: Always work from the `develop` branch. Never branch directly from `main`.
- **Naming Convention**: 
  - `feat/feature-name` for new capabilities.
  - `fix/bug-name` for fixes.
- **Merge Circuit**: 
  1. Working Branch -> `develop`.
  2. `develop` -> `main` (only after integration is stable).
- **Automation**: Do not manually update versions in `pyproject.toml`. The `release-please` automation handles versioning and changelogs on the `main` branch.