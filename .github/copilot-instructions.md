# Cerebellum — Copilot Instructions

You are assisting with **Cerebellum**: a production-grade, asynchronous, event-driven cognitive architecture framework for building AI agents. The LLM is one component of the reasoning engine — not the system itself.

This is an **enterprise-quality Python framework**. Every decision you make must reflect senior engineering discipline: correctness first, simplicity second, cleverness never.

All new features follow **Spec Driven Development (SDD)**. Read `.github/instructions/sdd.instructions.md` before implementing anything.

---

## 1. Architecture — The Non-Negotiables

Cerebellum is built on three immutable laws:

### Law 1 — The Event Bus is the only bridge
Cognitive modules (`Perception`, `Attention`, `Memory`, `Planners`, `Reasoning`, `Action`, `Learning`) **never** import or call each other directly. All communication flows through `EventBus` (`src/cerebellum/cognition/runtime/event_bus.py`).

Every module:
- inherits `CognitiveModule` and registers with `CognitiveRuntime`
- subscribes to input topics and publishes to output topics
- receives data only via `on_message(bus, payload)` — never via constructor injection from a sibling

Topic convention — lowercase, dot-separated:
```
perception.[process|output]
attention.[focused|set_focus]
memory.[store|recall|search]   →  memory.[available|stored]
reasoning.plan_ready
action.[completed]
```

### Law 2 — Cognition never touches Infrastructure
`src/cerebellum/cognition/` contains **pure brain logic**. It must never import `qdrant_client`, `httpx`, `axonium`, or any SDK directly.

Infrastructure adapters live in `src/cerebellum/infraestructure/`:
- `llm/llm_client.py` — wraps axonium, exposes `complete()` / `chat()`
- `llm/embedd_client.py` — wraps sentence-transformers
- `storage/db_episodic.py` — wraps `AsyncQdrantClient`
- `observability/tracer.py`, `observability/metrics.py`

### Law 3 — Async everywhere, no exceptions
All I/O is `async def` / `await`. Zero tolerance for:
- `requests` → use `httpx.AsyncClient`
- `time.sleep` → use `asyncio.sleep`
- sync Qdrant client → use `AsyncQdrantClient`
- **Blocking CPU in async context** → use `await asyncio.to_thread(fn, *args)` for CPU-bound calls like `sentence-transformers` encode

---

## 2. Type System & Data Contracts

- Python 3.13+. Every function, method, and class attribute has a type annotation.
- `mypy src` must pass with **0 errors** before any PR. No exceptions.
- `Any` is forbidden except at external JSON/dict boundaries — always coerce to a `pydantic.BaseModel` inside the infrastructure layer.
- All cross-module event payloads are `pydantic.BaseModel` subclasses defined in `src/cerebellum/cognition/runtime/protocols.py`. Never pass raw `dict` across module boundaries.
- All cognitive data structures (Plan, PerceptionResult, Thought) are defined in `src/cerebellum/cognition/core/models.py`.

---

## 3. Codebase Baseline — Pre-SDD Audit (May 2026)

This section reflects the state of the codebase before SDD specs began. Use this as the ground truth for what to keep, fix, or remove.

### ✅ Keep as-is (production-ready)

| Module | Path |
|--------|------|
| CognitiveRuntime | `cognition/runtime/cognitive_runtime.py` |
| EventBus | `cognition/runtime/event_bus.py` |
| Protocols + Types | `cognition/runtime/protocols.py`, `types.py` |
| TextPerception | `cognition/perception/text_perception.py` |
| SimpleAttention | `cognition/attention/simple_attention.py` |
| WorkingMemory | `cognition/memory/working_memory.py` |
| EpisodicMemory | `cognition/memory/episodic_memory.py` |
| SemanticMemory | `cognition/memory/semantic_memory.py` |
| SimplePlanner + LLMPlanner | `cognition/planners/` |
| MotorCortex | `cognition/action/motor_cortex.py` |
| SimpleLearning | `cognition/learning/simple_learning.py` |
| Neural + LLMNeural | `cognition/neural/` |
| Symbolic engine | `cognition/symbolic/` (compiler, constraints, rules) |
| LLMClient | `infraestructure/llm/llm_client.py` |
| EmbeddingClient | `infraestructure/llm/embedding.py` |
| DbEpisodic | `infraestructure/storage/db_episodic.py` |
| CognitiveAgent | `cognition/core/agent.py` |
| Core models | `cognition/core/models.py` |

### 🔧 Must fix before any new spec

| Issue | File | Fix |
|-------|------|-----|
| **Blocking CPU in async** — `self._model.encode()` called in `async def` without `to_thread` | `infraestructure/llm/embedd_client.py` | `await asyncio.to_thread(self._model.encode, text)` |
| **`print()` statement** in production code | `infraestructure/observability/tracer.py` | Replace with `logger.debug()` |
| Observability stubs not integrated into the cognitive loop | `infraestructure/observability/` | Wire tracer into CognitiveRuntime steps |

### ❌ Dead code — delete

| File | Reason |
|------|--------|
| `cognition/runtime/event_loop.py` | Unused — logic lives in CognitiveRuntime |
| `cognition/runtime/rules.py` | Orphaned — real rules in `symbolic/` |
| `cognition/perception/multimodal_perception.py` | Empty stub |
| `cognition/planners/task_graph_planner.py` | Empty stub |
| `tools/code_executor.py` | Empty stub |

### 📋 Not yet implemented (reserved for future specs)

| Capability | Location | Notes |
|-----------|----------|-------|
| Metacognition | `cognition/metacognition/` | Folder exists, no implementation |
| Procedural memory | `cognition/memory/` | Described in README, not built |
| Observability wiring | `infraestructure/observability/` | Tracer/metrics exist but not called |
| HTTP API layer | — | Not started |

---

## 4. Quality Gates

Every code change must pass all of the following before being considered complete:

```bash
uv run mypy src          # 0 errors
uv run ruff check .      # 0 warnings
uv run pytest tests/ -v  # all pass
```

No exceptions. Fix the gate, not the check.

---

## 5. Testing Standards

- `pytest` + `@pytest.mark.asyncio` for all async tests.
- Never call real external services (Qdrant, LLM servers, HTTP APIs) in unit tests. Always use `AsyncMock`.
- One test per AC minimum. Naming: `test_<description>_AC<N>`.
- Mock target: the infrastructure boundary, not the cognition layer.

```python
with patch(
    "cerebellum.infraestructure.storage.db_episodic.AsyncQdrantClient.search",
    new_callable=AsyncMock,
) as mock_search:
    ...
```

---

## 6. Observability & Logging

- **Zero `print()` statements** in any production path.
- Logger: `logging.getLogger("cerebellum.<domain>")` where domain matches the cognitive module (e.g. `cerebellum.perception`, `cerebellum.memory.episodic`).
- Log levels:
  - `.debug` — internal state, payload contents
  - `.info` — cognitive phase transitions (perception done, plan created, action completed)
  - `.warning` — degraded operation, fallback triggered
  - `.error` — unrecoverable failures, always with `exc_info=True`
- Tracer spans: `src/cerebellum/infraestructure/observability/tracer.py`, span names follow `<domain>.<action>` (e.g. `perception.process`, `memory.recall`).

---

## 7. HTTP Endpoints (when added)

- Use `FastAPI`. All route handlers are `async def`.
- Error responses **must follow RFC 9457 Problem Details** (`application/problem+json`). Required fields: `type`, `title`, `status`, `detail`. Optional: `instance`.
- Never expose internal stack traces, exception messages, or model internals in HTTP responses.
- Authentication and scope checks must be performed in middleware or a dedicated dependency — never inside business logic.

---

## 8. Security

- Secrets (LLM base URL, API keys, Qdrant credentials) come from environment variables only. Never hardcoded, never in source.
- Never log LLM prompts, task strings, or completions if they may contain PII.
- Never pass raw LLM output directly to tool execution without pydantic validation first.
- Never derive infrastructure URLs (Qdrant host, LLM endpoint) from user input or LLM output.
- Tool inputs (`web_search`, `database_tool`) must be validated with pydantic before execution.

---

## 9. Dependency Discipline

Declared in `pyproject.toml`. Already available: `asyncio`, `pydantic`, `qdrant-client`, `axonium`, `fastapi`, `sentence-transformers`, `pytest`, `mypy`, `ruff`.

- Add new dependencies only when a spec explicitly requires them.
- Install via `uv pip install --system -e .[dev]`. Never bare `pip install`.
- Prefer stdlib and existing deps over new ones.

---

## 10. Branching & SDD Workflow

- Base branch: `develop`. Never branch from `main`.
- Branch names: `feat/NNN-kebab-title`, `fix/NNN-kebab-title`, `hotfix/NNN-kebab-title`.
- **No feature code without an approved spec** (`status: approved` in `memory/specs/NNN-*.md`).
- Versioning is automated via `release-please`. Never edit `version` in `pyproject.toml` manually.

Full SDD pipeline: `.github/instructions/sdd.instructions.md`
