# core/agent.py
import uuid
from typing import Any
from cerebellum.cognition.runtime.types import Message
from ..runtime import CognitiveRuntime


class CognitiveAgent:
    """A wrapper for the cognitive system (CognitiveRuntime)."""

    def __init__(self, runtime: CognitiveRuntime) -> None:
        self.runtime = runtime

    async def run(self, topic: str, payload: dict) -> Any:
        """Publishes a task/stimulus to the system's message bus."""
        msg = Message(
            id=str(uuid.uuid4()),
            sender="agent_interface",
            receiver="broadcast",
            topic=topic,
            payload=payload,
            correlation_id=str(uuid.uuid4())
        )
        return await self.runtime.publish(msg)