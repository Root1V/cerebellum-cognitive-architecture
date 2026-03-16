# Coding Rules

**Language:** Python 3.13+

## Rules
- **Async-First:** All asynchronous IO must use `async`/`await`.
- **Loose Coupling:** Modules must not depend directly on concrete implementations of other major components.
- **Type Checking:** All methods and functions require strict Python type hints validating against `mypy` without `Any` overrides when possible.

## Structure
The source code organizes into `cognition` (brain logic) and `infrastructure` (connections to the outside world):

```text
src/
└── cerebellum/
    ├── cognition/
    │   ├── action/
    │   ├── attention/
    │   ├── core/
    │   ├── learning/
    │   ├── memory/
    │   ├── perception/
    │   ├── planners/
    │   ├── reasoning/
    │   └── runtime/
    └── infrastructure/
        ├── llm/
        ├── observability/
        ├── security/
        └── storage/
```

## Logging
- Never use basic `print()`.
- Use structured logging via the standard `logging` library.
- Configure loggers using `logging.getLogger("cerebellum.module")`.