---
id: "002"
title: "Remove Dead Code & Fix Production Issues"
status: tests-passed
current-agent: test-agent
created: 2026-06-01T00:53:29Z
updated: 2026-06-01T00:59:12Z
branch: feat/002-remove-dead-code-fix-production-issues
base-branch: develop
pipeline-log:
  - agent: spec-writer-agent
    status: draft
    timestamp: 2026-06-01T00:53:29Z
  - agent: developer-agent
    status: implementing
    timestamp: 2026-06-01T00:55:49Z
  - agent: developer-agent
    status: code-complete
    timestamp: 2026-06-01T00:57:14Z
  - agent: test-agent
    status: tests-passed
    timestamp: 2026-06-01T00:59:12Z
---

# 002 — Remove Dead Code & Fix Production Issues

## Problem Statement

The codebase contains five stub or orphaned source files that contribute no behaviour and import nothing useful, plus one `print()` statement in a production observability module that violates the zero-`print` rule. These issues:

- **Dead files**: increase surface area for future confusion, shadow real implementations (e.g. `rules.py` conflicts with `symbolic/rules.py`), and silently bloat the package.
- **`print()` in tracer**: violates the project-wide rule that all output must go through `logging`; makes traces invisible to log aggregators and breaks `ruff` compliance if the lint rule is ever enabled.

**Who is affected:** Every developer and agent that reads or extends the codebase.

## Goals

- [ ] Delete all 5 dead/stub files cleanly with no import breakage
- [ ] Replace the single `print()` in `tracer.py` with a `logger.debug()` call
- [ ] Confirm all existing tests still pass after deletion

## Non-Goals

- Not integrating the tracer into the cognitive loop (that is spec 003)
- Not adding new test coverage beyond confirming no regressions
- Not refactoring any logic in surviving files

## Proposed Solution

### Files to delete

| File | Reason |
|------|--------|
| `src/cerebellum/cognition/runtime/event_loop.py` | Defines `CognitiveEventLoop` (a bare `while True: sleep(0.01)` stub). Not imported anywhere. Logic lives in `CognitiveRuntime`. |
| `src/cerebellum/cognition/runtime/rules.py` | Defines `RuleEnginePort` ABC. Not imported anywhere. Duplicate concern — real rule engine is in `cognition/symbolic/`. |
| `src/cerebellum/cognition/perception/multimodal_perception.py` | Empty file. No exports, no callers. |
| `src/cerebellum/cognition/planners/task_graph_planner.py` | Empty file. Not in `planners/__init__.py`, no callers. |
| `src/cerebellum/tools/code_executor.py` | Empty file. Not in `tools/__init__.py`, no callers. |

None of these appear in any `__init__.py` or are imported by any other module (confirmed by grep).

### File to modify

`src/cerebellum/infraestructure/observability/tracer.py` — line 8:

**Before:**
```python
print(f"[TRACE] {event}: {data}")
```

**After:**
```python
logger.debug("[TRACE] %s: %s", event, data)
```

Add at module top:
```python
import logging
logger = logging.getLogger("cerebellum.observability.tracer")
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Delete, not comment out | Dead files waste grep space and invite confusion; commenting is not a substitute for deletion |
| `logger.debug` not `logger.info` | Trace payloads are high-frequency internal state — debug is the correct level per project logging policy |
| No `__init__.py` changes needed | None of the 5 deleted files are re-exported via any `__init__.py` |

## API Contract

No API contract changes. No public symbols are removed.

## Data Model

No data model changes.

## Security Considerations

- No secrets or credentials involved.
- Removing `print()` from the tracer eliminates the risk of accidentally leaking trace payloads (which may include task strings or memory content) to stdout in production environments where stdout is captured by log shippers.
- No new code paths or attack surface introduced.

## Acceptance Criteria

- [x] AC-1: Given the 5 dead files are deleted, when `git status` is checked, then none of those 5 paths exist in the working tree.
- [x] AC-2: Given the deletions are applied, when `uv run python -c "import cerebellum"` is executed, then it exits with code 0 and no ImportError.
- [x] AC-3: Given `tracer.py` is modified, when `grep -r "print(" src/` is executed, then it returns no matches.
- [x] AC-4: Given `tracer.py` is modified, when `Tracer().trace("test", {"key": "value"})` is called, then it logs via `logging.getLogger("cerebellum.observability.tracer")` at DEBUG level instead of printing to stdout.
- [x] AC-5: Given all changes are applied, when `uv run mypy src` is executed, then it exits with 0 errors.
- [x] AC-6: Given all changes are applied, when `uv run ruff check .` is executed, then it exits with 0 warnings.
- [x] AC-7: Given all changes are applied, when `uv run pytest tests/ -v` is executed, then all existing tests pass with no regressions.

## E2E Validation

> No full-stack validation script required — this spec only deletes files and removes a `print()`. Quality gates (mypy, ruff, pytest) are sufficient.

## Open Questions

- None
