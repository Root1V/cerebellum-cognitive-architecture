# Permite actuar en el mundo.
# Ejemplos:
# call API
# execute code
# search web
# query database
# control robot

# cognition/action.py

from abc import ABC, abstractmethod


class Action(ABC):

    @abstractmethod
    async def execute(self, task):
        """
        Execute action in environment.
        """
        ...