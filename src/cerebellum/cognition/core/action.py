# Permite actuar en el mundo.
# Ejemplos:
# call API
# execute code
# search web
# query database
# control robot

# cognition/action.py

from abc import ABC, abstractmethod
from typing import Any


class Action(ABC):

    @abstractmethod
    async def execute(self, task: Any) -> Any:
        """
        Execute action in environment.
        """
        ...