# Coding Rules

Language: Python

Rules:

- async-first programming
- all IO must be async
- modules must be loosely coupled

Structure:

src/
    cerebellum/
      cognition/
        perception/
        attention/
        core/
        learning/
        memory/
        reasoning/
        planners/
        action/
        runtime/
      infrastructure/
        llm/
        observability/
        storage/
        security/

Logging:

Use structured logging.