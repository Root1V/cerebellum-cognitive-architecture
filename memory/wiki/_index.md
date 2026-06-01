# Wiki — Cerebellum Knowledge Index

This is the authoritative catalog of all wiki pages and decision files in `memory/`.

`wiki-sync-agent` and `docs-agent` MUST read this file before creating or updating pages.

---

## Wiki Pages

| Page | Topic |
|------|-------|
| [architecture.md](architecture.md) | Cognitive loop, module responsibilities, event bus design |
| [event-bus.md](event-bus.md) | Event Bus internals, topic conventions, payload protocols |
| [memory-system.md](memory-system.md) | Working, Episodic, Semantic, Procedural memory abstractions and storage |
| [llm-adapter.md](llm-adapter.md) | axonium SDK integration, LLMClient usage, embedding client |
| [observability.md](observability.md) | Tracer, metrics, logging conventions |
| [tools.md](tools.md) | Available tools (web_search, code_executor, database_tool), tool interface |
| [testing.md](testing.md) | Test strategy, mock patterns, how to run the test suite |
| [deployment.md](deployment.md) | Docker, environment variables, startup order |

---

## Decisions

| File | Decision |
|------|---------|
| [2026-05-31-event-bus-as-only-bridge.md](../decisions/2026-05-31-event-bus-as-only-bridge.md) | All cross-module communication flows through EventBus — no direct module coupling |
| [2026-05-31-async-first-io.md](../decisions/2026-05-31-async-first-io.md) | All I/O must be async — no synchronous network or DB calls |
| [2026-05-31-pydantic-for-all-payloads.md](../decisions/2026-05-31-pydantic-for-all-payloads.md) | All event bus payloads and cross-module data structures use pydantic BaseModel |

---

## How to use this index

- `docs-agent`: after a spec is `human-approved`, update only the pages listed above that are affected by the spec changes.
- `wiki-sync-agent`: scan all closed specs and update only pages where cross-cutting facts are missing or stale.
- **Never rewrite an entire page** — make targeted, minimal edits.
- **Keep each page under ~150 lines.**
- After editing any page, append one line to `_hot.md`.
