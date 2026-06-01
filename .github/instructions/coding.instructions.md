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
    ├── cognition/        # Pure business/neuro-logic. Independent of infrastructure.
    │   ├── action/           # Motor cortex — produces environmental effects post-reasoning
    │   ├── attention/        # Filters perceptions using semantic relevance
    │   ├── core/             # Abstract Base Classes (ABCs) and Pydantic models (models.py, agent.py)
    │   ├── learning/         # Evaluates outcomes to update future planning
    │   ├── memory/           # Working, Episodic, Semantic, ProceduralMemory abstractions
    │   ├── perception/       # Normalises raw inputs into structured PerceptionResult
    │   ├── planners/         # SimplePlanner, LLMPlanner, TaskGraphPlanner
    │   ├── runtime/          # CognitiveRuntime, EventBus, MessageBus, protocols.py, types.py, rules.py
    │   ├── symbolic/         # Symbolic reasoning: compiler, constraints, rules
    │   ├── metacognition/    # (reserved) self-monitoring and meta-level reasoning
    │   └── neural/           # LLM neural reasoning wrappers (llm_neural.py)
    └── infraestructure/  # Concrete real-world implementations (note: spelled as in project)
        ├── llm/              # Wrappers for axonium SDK (llm_client.py, llm.py, embedding.py)
        ├── observability/    # Tracer and metrics (tracer.py, metrics.py)
        ├── security/         # (reserved) Auth, encryption
        └── storage/          # Qdrant adapters (db_episodic.py, db_memory.py)
```

## 5. Logging and Observability
* **Prohibited:** `print()` statements for debugging or standard output.
* **Rule:** Use structured logging via the standard `logging` library.
* **Setup:** `logger = logging.getLogger("cerebellum.<module>")` where `<module>` matches the cognitive domain (e.g. `cerebellum.perception`, `cerebellum.memory`, `cerebellum.runtime`). Use `.debug` for verbose tracking, `.info` for cognitive phase transitions, and `.error` for exceptions. Always include context when logging (e.g. `logger.error("Plan execution failed", exc_info=True)`).

## 6. Running the Project

```bash
# Install dependencies
uv pip install --system -e .[dev]

# Run all tests
uv run pytest tests/ -v

# Type check
uv run mypy src

# Lint
uv run ruff check .

# Start the system
uv run python main.py
```.