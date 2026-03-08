# core/environment.py

from abc import ABC, abstractmethod


class Environment(ABC):

    @abstractmethod
    def observe(self):
        """Return current state of the environment."""
        pass

    @abstractmethod
    def update(self, action):
        """Apply an action result to the environment."""
        pass
