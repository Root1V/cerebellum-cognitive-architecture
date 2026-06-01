# Cerebellum — Copilot Instructions

Cerebellum is an async, event-driven cognitive framework. Follow SDD: no feature code before an approved spec.

## Rules
- Base branch: `develop`; branch names: `feat/NNN-*`, `fix/NNN-*`, `hotfix/NNN-*`.
- Cognition only talks through `EventBus`; no direct sibling imports/calls.
- Cognition must not import infrastructure SDKs directly; use `infraestructure/*` adapters.
- All I/O is `async`/`await`; use `asyncio.to_thread()` for blocking CPU work.
- Use type hints everywhere; `mypy src` must stay at 0 errors.
- Cross-module payloads are `pydantic.BaseModel`; no raw `dict` across module boundaries.
- Never use `print()` in production; use `logging.getLogger("cerebellum.<domain>")`.
- Keep logs safe: no secrets, prompts, or PII.

## Testing
- Use `pytest` + `@pytest.mark.asyncio` for async code.
- Mock external services with `AsyncMock`; never hit real LLM/DB/HTTP services in unit tests.
- Minimum one test per AC when specs introduce behavior.

## Quality Gates
```bash
uv run mypy src
uv run ruff check .
uv run pytest tests/ -v
```

## Keep in Mind
- Dead code should be deleted, not commented out.
- HTTP APIs (when added) must use FastAPI and RFC 9457 Problem Details.
- Add dependencies only when a spec requires them.
