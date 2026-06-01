# Specs — Cerebellum SDD

This directory contains all SDD specs for the Cerebellum cognitive architecture framework.

## Status Legend

| Status | Meaning |
|--------|---------|
| `draft` | Being written — awaiting human approval |
| `approved` | Cleared for implementation |
| `implementing` | AC implementation in progress |
| `code-complete` | All ACs implemented — awaiting test validation |
| `testing` | Tests being written and run |
| `tests-passed` | All tests green — awaiting security review |
| `reviewing` | Security review in progress |
| `security-approved` | No CRITICAL/HIGH findings — awaiting human review |
| `human-approved` | Deliverable reviewed and accepted — cleared for docs |
| `documenting` | Docs and spec reconciliation in progress |
| `implemented` | Spec reconciled, AGENTS.md and wiki updated |
| `releasing` | Commit · push · PRs · tag · release in progress |
| `released` | Merged to main, tagged, GitHub release created |
| `closed` | Fully released and closed |

## Spec Index

| ID | Title | Status | Branch |
|----|-------|--------|--------|
| [001](001-fix-blocking-io-embedding-client.md) | Fix Blocking I/O in EmbeddingClient | closed | feat/001-fix-blocking-io |
| [002](002-remove-dead-code-fix-production-issues.md) | Remove Dead Code & Fix Production Issues | implemented | feat/002-remove-dead-code-fix-production-issues |

---

## Backlog

See [backlog.md](backlog.md) for the prioritized list of specs to create based on pre-SDD codebase audit.

## Naming Convention

```
NNN-kebab-case-name.md
```

- `NNN` is zero-padded and sequential: `001`, `002`, `003`, …
- Never rename a spec after it reaches `approved`.
- Never reuse a spec number.

## Branching

| Spec type | Branch pattern | Base |
|-----------|---------------|------|
| Feature | `feat/NNN-kebab-title` | `develop` |
| Fix | `fix/NNN-kebab-title` | `develop` |
| Hotfix | `hotfix/NNN-kebab-title` | `main` |
