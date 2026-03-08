# memory/working_memory.py


from ..core.memory import Memory

class WorkingMemory(Memory):

    def __init__(self):
        self.state = {}

    async def store(self, key, value):
        self.state[key] = value

    async def retrieve(self, key):
        return self.state.get(key)

    async def update(self, item):
        if isinstance(item, dict):
            self.state.update(item)