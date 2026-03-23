# core/agent.py
import uuid
import warnings
from typing import Any, Optional
from cerebellum.cognition.runtime.types import Message
from ..runtime import CognitiveRuntime


class CognitiveAgent:
    """
    CognitiveAgent
    --------------
    A high-level wrapper for interacting with the cognitive architecture.
    Provides a simpler interface for agents / human-in-the-loop to 
    publish tasks to the system.
    """

    def __init__(self, runtime: Optional[CognitiveRuntime] = None, **kwargs: Any) -> None:
        """
        Initializes the agent with a CognitiveRuntime instance.
        
        Args:
            runtime: The CognitiveRuntime instance to use.
            **kwargs: Used for backward compatibility with 'cognitive_system'.
        """
        # Backward compatibility with 'cognitive_system'
        if "cognitive_system" in kwargs:
            warnings.warn(
                "The 'cognitive_system' argument is deprecated. Use 'runtime' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            self.runtime = kwargs["cognitive_system"]
        elif runtime:
            self.runtime = runtime
        else:
            raise ValueError("A 'runtime' instance is required.")

    async def run(self, topic_or_task: str, payload_or_context: Optional[dict] = None) -> Any:
        """
        Publishes a task or stimulus to the system's message bus.
        
        Supports two signatures:
        1. run(task: str) -> Standard task/perception processing.
        2. run(topic: str, payload: dict) -> Publishing to a specific topic.
        """
        # Interpretation of arguments
        if payload_or_context is None:
            # Old signature: run(task)
            topic = "perception.process"
            payload = {"input_type": "text", "raw_data": topic_or_task}
        else:
            # New signature: run(topic, payload)
            topic = topic_or_task
            payload = payload_or_context

        msg = Message(
            id=str(uuid.uuid4()),
            sender="agent_interface",
            receiver="broadcast",
            topic=topic,
            payload=payload,
            correlation_id=str(uuid.uuid4())
        )
        
        # NOTE: CognitiveAgent.run as a method might want to 'run' and wait for result if possible.
        # But our system is purely asynchronous. For common patterns, publishing is the way.
        return await self.runtime.publish(msg)