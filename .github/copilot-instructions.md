# Copilot Instructions

When writing code for this project:

## Always
- Use best practice and enterprise practice
- Use Python async/await
- Use strict type hints (`mypy` compliant)
- Follow modular architecture
- Create small composable modules

## Avoid
- Synchronous network calls
- Blocking IO operations
- Tight coupling between modules

## When creating cognitive components
- Always connect to the `EventBus`
- Never call other modules directly (use the message bus)

## When writing tests
- Use `pytest`
- Use `@pytest.mark.asyncio` to test async functions
- Mock external dependencies (`Qdrant`, LLMs, etc.)