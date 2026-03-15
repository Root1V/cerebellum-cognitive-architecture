# Copilot Instructions

When writing code for this project:

Always:

- use best practice and enterprise practice
- use Python async/await
- use type hints
- follow modular architecture
- create small composable modules

Avoid:

- synchronous network calls
- blocking IO
- tight coupling between modules

When creating cognitive components:

- always connect to the EventBus
- never call other modules directly

When writing tests:

- use pytest
- test async functions