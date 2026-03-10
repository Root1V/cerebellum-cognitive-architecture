# core/learning.py

# Permite mejorar con la experiencia.
# Aprende de:
# resultados
# errores
# feedback
# éxitos

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Experience:
    """Represents a single learning experience for the cognitive agent.

    Attributes:
        result: The outcome or output produced by the agent's action.
        error: An exception or error message if the action failed, or None.
        feedback: External feedback provided about the action (e.g. user rating,
            evaluation score, or a descriptive string).
        success: Whether the action is considered successful.
        timestamp: UTC datetime when the experience was recorded.
        context: Optional arbitrary context data associated with the experience
            (e.g. task description, environment state).
    """

    result: Any
    error: Exception | str | None
    feedback: Any
    success: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: dict[str, Any] | None = None


class Learning(ABC):
    """Abstract base class for the learning subsystem of the cognitive agent.

    Concrete implementations must integrate experience-driven adaptation so
    that the agent improves its behaviour over time.  All methods are
    asynchronous to remain consistent with the rest of the cognitive
    architecture.

    Example:
        >>> class MyLearning(Learning):
        ...     async def update(self, experience: Experience) -> None:
        ...         ...
        ...     async def get_insights(self) -> dict[str, Any]:
        ...         return {}
        ...     async def reset(self) -> None:
        ...         ...
    """

    @abstractmethod
    async def update(self, experience: Experience) -> None:
        """Update the internal knowledge base with a new experience.

        Args:
            experience: An :class:`Experience` instance containing the result,
                error, feedback, and success flag for a completed action.
        """
        ...

    @abstractmethod
    async def get_insights(self) -> dict[str, Any]:
        """Return accumulated learnings and patterns.

        Returns:
            A dictionary mapping insight keys to their values.  The exact
            structure is determined by the concrete implementation.
        """
        ...

    @abstractmethod
    async def reset(self) -> None:
        """Clear all accumulated learning state.

        Useful for testing and for agent lifecycle management (e.g. starting
        a fresh episode without carrying over previous knowledge).
        """
        ...