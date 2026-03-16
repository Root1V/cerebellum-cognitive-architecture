# Coding Rules

**Language:** Python 3.13+

These rules ensure code remains fast, modern, strictly typed, and enterprise-ready.

## 1. Async-First Programming
* **Rule:** All asynchronous IO must use `async` / `await`.
* **Prohibited:** Utilizing synchronous networking or sleep functions (`requests`, `time.sleep`, synchronous DB drivers). Use `httpx`, `asyncio.sleep`, and `qdrant_client.AsyncQdrantClient`.
* **Testing:** Any IO or cognitive process must be tested with `@pytest.mark.asyncio`, using `AsyncMock` to isolate network boundaries.

## 2. Strict Type Hinting (Mypy Compliant)
* Every function, method parameter, and return type MUST have a type hint.
* **Prohibited:** Avoiding types, or abusing `from typing import Any` just to quickly pass validation. Use `Any` exclusively when reading flexible external json schemas, but always coerce to `pydantic.BaseModel` within the boundary.
* If a third-party module lacks typing, use `# type: ignore[import-untyped]` intentionally.

## 3. Data Integrity with Pydantic
* The system utilizes `pydantic` heavily in `src/cerebellum/cognition/core/models.py`.
* When passing events or data between core systems (like from Planner to Reasoner), construct and use a `Plan` model rather than a raw `list[dict]`.

## 4. Directory Structure Enforcement
```text
src/
└── cerebellum/
    ├── cognition/        # Pure business/neuro-logic. Independent of tools.
    │   ├── action/
    │   ├── attention/
    │   ├── core/         # Abstract Base Classes (Interfaces) and Pydantic Models
    │   ├── learning/
    │   ├── memory/       # Working, Semantic, Memory Stream abstraction
    │   ├── perception/
    │   ├── planners/
    │   ├── reasoning/
    │   └── runtime/      # Event Bus and System Orchestration
    └── infrastructure/   # The dirty real-world implementations
        ├── llm/          # Wrappers for axonium, Transformers, OpenAI
        ├── observability/# Metrics, logging adapters
        ├── security/     # Auth, encryption
        └── storage/      # Vector databases (Qdrant), SQL, File Systems
```

## 5. Logging and Observability
* **Prohibited:** `print()` statements for debugging or standard output.
* **Rule:** Use structured logging via the standard `logging` library.
* **Setup:** `logger = logging.getLogger("cerebellum.module")`. Use `.debug` for verbose tracking, `.info` for cognitive shifts, and `.error` for exceptions. Include context when logging (e.g., `logger.error("Failed executing plan", exc_info=True)`).