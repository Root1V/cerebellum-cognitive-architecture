# Relación correcta
# La relación correcta es:
# Reasoner
#    │
#    ▼
# Action
#    │
#    ├── Tool
#    └── Environment
# Es decir:
# Action decide qué hacer
# Tool es un recurso que puede usar
# Environment es el mundo donde actúa

from ..core.action import Action
from ..core.tool import Tool


class ConsoleAction(Action):

    def __init__(self, tools: dict[str, Tool] | None = None):
        self.tools: dict[str, Tool] = tools or {}

    async def execute(self, action):

        if isinstance(action, list):
            for item in action:
                print(f"[ACTION] {item}")
            return action

        if isinstance(action, dict):
            if action.get("type") == "tool":
                tool = self.tools.get(action["tool"])
                if tool:
                    return await tool.execute(**action.get("input", {}))

            if action.get("type") == "respond":
                print(f"[RESPOND] {action['content']}")
                return action["content"]

        print(f"[ACTION] {action}")
        return action
