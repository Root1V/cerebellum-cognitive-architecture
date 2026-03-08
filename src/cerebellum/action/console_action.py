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

from ..core.tool import Tool

class ConsoleAction:

    def __init__(self, tools: list[Tool], environment):
        self.tools = tools
        self.environment = environment
        
    def execute(self, action):

        if action["type"] == "tool":

            tool = self.tools[action["tool"]]

            return tool.run(action["input"])

        if action["type"] == "respond":

            return action["content"]
