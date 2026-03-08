from typing import Any

from cerebellum.core.learning import Experience, Learning


class SimpleLearning(Learning):
    """Minimal in-memory implementation of the :class:`Learning` interface.

    Stores all experiences in a list and exposes basic insights such as
    success rate and total experience count.
    """

    def __init__(self) -> None:
        self._experiences: list[Experience] = []

    async def update(self, experience: Experience) -> None:
        """Append *experience* to the internal experience log.

        Args:
            experience: The :class:`Experience` to record.
        """
        self._experiences.append(experience)

    async def get_insights(self) -> dict[str, Any]:
        """Return simple statistics derived from recorded experiences.

        Returns:
            A dictionary with:
            - ``total``: total number of recorded experiences.
            - ``success_rate``: fraction of successful experiences (0.0 if none).
            - ``last_result``: the result of the most recent experience, or
              ``None`` if no experiences have been recorded.
        """
        total = len(self._experiences)
        if total == 0:
            return {"total": 0, "success_rate": 0.0, "last_result": None}

        successes = sum(1 for e in self._experiences if e.success)
        return {
            "total": total,
            "success_rate": successes / total,
            "last_result": self._experiences[-1].result,
        }

    async def reset(self) -> None:
        """Clear all recorded experiences."""
        self._experiences.clear()
    