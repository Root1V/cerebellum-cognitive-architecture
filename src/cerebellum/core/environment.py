# core/environment.py

from abc import ABC, abstractmethod


class Environment(ABC):

    @abstractmethod
    def observe(self) -> dict:
        """Return current state of the environment."""
        pass

    @abstractmethod
    def update(self, action: dict) -> None:
        """Apply an action result to the environment."""
        pass
