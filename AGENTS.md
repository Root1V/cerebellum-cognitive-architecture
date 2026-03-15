# AGENTS.md

## Project Overview

This project implements a cognitive system inspired by neuroscience.

The system is built as a distributed asynchronous event-driven architecture.

Core design principles:

- asynchronous execution
- event driven communication
- modular cognitive components
- high parallelism

## Cognitive modules

The system contains the following cognitive subsystems:

1. Perception
2. Attention
3. Memory
4. Reasoning
5. Planning
6. Action
7. Learning

Each subsystem communicates through the Event Bus.

## Development stack

Language:
Python 3.13

Core libraries:

- asyncio
- fastapi
- pydantic
- qdrant

## Architecture rules

All cognitive modules:

- must be asynchronous
- communicate through the EventBus
- must not call other modules directly

## Running the project

### Install UV:

- pip install uv

### Instalar axonium (SDK propio) desde repo público
- uv pip install --system git+https://github.com/Root1V/axonium-sdk.git@main

### Install dependencies with uv
- uv pip install --system -e .[dev]

Run system:

python main.py

## Testing

pytest tests/

## Code guidelines

- use type hints
- avoid blocking IO
- keep modules small
- log all events