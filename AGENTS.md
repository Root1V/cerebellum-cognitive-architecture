# Cerebellum - AI Agent & Developer Guidelines (AGENTS.md)

This file (`AGENTS.md`) serves as the foundational rulebook for all human contributors, AI pair programmers (Cursor, Cline, Aider, etc.), and Autonomous Agents operating on the `cerebellum` codebase.

## 🧠 Project Overview
**Cerebellum** is a distributed, asynchronous, event-driven cognitive architecture heavily inspired by human neuroscience. We are building the brain of a digital entity.

**Core Design Principles:**
1. **Asynchronous Execution:** The brain never sleeps, and neither does IO. 
2. **Event-Driven Choreography:** No central orchestrator. Synapses (messages) fire and lobes react independently.
3. **Modular Cognitive Components:** Decoupled, specialized neuro-lobes.
4. **High Parallelism:** Thinking, perceiving, and remembering happen concurrently.

---

## 🏗 Cognitive Subsystems
Our "brain logic" lives in `src/cerebellum/cognition/` and is divided into distinct domains. **No module can instantiate or directly call another.**
1. **Perception**: Extracts structured reality (`PerceptionResult`). Listens for `perception.process`, emits `perception.output`.
2. **Attention**: Filters perceptions using semantic relevance. Listens for `perception.output` and `attention.set_focus`, emits `attention.focused`.
3. **Memory**: Working, Episodic, and Semantic stores. Listens for `memory.store`, `memory.recall`, `memory.search`. Emits `memory.available` or `memory.stored`.
4. **Reasoning/Planning**: The prefrontal cortex. Listens for `attention.focused`, uses LLMs to generate `Plan` objects. Emits `reasoning.plan_ready`.
5. **Action**: The motor cortex. Listens for `reasoning.plan_ready`, executes step-by-step tools and actuators. Emits `action.completed`.
6. **Learning**: Evaluates Action outcomes against expectations to optimize future planning.

---

## 🛠 Technology Stack
* **Language:** Python 3.13+
* **Concurrency:** `asyncio`
* **Data Validation:** `pydantic`
* **APIs / System Orchestration:** `fastapi`
* **Vector Storage:** `qdrant-client` (Async mode exclusively)
* **LLM Engine:** `axonium` (Our custom SDK for local/server inference)

---

## ⚖️ Immutable Architecture Rules
Any AI or Human submitting a Pull Request MUST adhere to the following:
1. **Async-First:** Absolutely NO synchronous network calls (`requests`. `urllib`) or blocking sleep (`time.sleep`).
2. **EventBus Dependency:** All cross-module chatter happens over the Event Bus. **Zero direct method invocation between sibling cognitive lobes.**
3. **Strict Typing:** All code must pass `mypy src` with 0 errors. Avoid `Any` in favor of `pydantic` base models.
4. **Clean Testing:** Tests live in `tests/unit` and `tests/integration`. Use `@pytest.mark.asyncio`. NEVER hit external systems (LLMs, DBs) during unit tests; always patch and `AsyncMock` them.
5. **Payload Protocols**: All message payloads MUST use `pydantic` models defined in `src/cerebellum/cognition/runtime/protocols.py`.

---

## 🌿 Git Flow & Branching Strategy
We use a structured branching model to maintain stability:
1. **`main`**: Production-ready code. Only modified via automated Release PRs.
2. **`develop`**: The integration branch. All feature branches start from here and merge back here.
3. **`feat/*` & `fix/*`**: Working branches. Always created relative to `develop`.
4. **Releases**: Managed by `release-please`. Merging `develop` into `main` triggers an automated Release PR. Merging that PR generates the tag and Docker image.

**Cleanup Rule:** Head branches are automatically deleted upon successful merge to keep the repo clean.

---

## 🚀 Running the Project (Dev Setup)

**1. Install UV (The modern Python package manager):**
```bash
pip install uv
```

**2. Install our custom LLM SDK (axonium):**
```bash
uv pip install --system git+https://github.com/Root1V/axonium-sdk.git@main
```

**3. Install Project Dependencies:**
```bash
uv pip install --system -e .[dev]
```

**4. Run Tests:**
```bash
uv run pytest tests/ -v
```

**5. Check Types & Linting:**
```bash
uv run mypy src
uv run ruff check .
```

**6. Start the System:**
```bash
uv run python main.py
```