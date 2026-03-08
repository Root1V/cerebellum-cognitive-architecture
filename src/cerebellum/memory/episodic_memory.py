# memory/episodic_memory.py

class EpisodicMemory:

    def __init__(self):
        self.events = []

    async def store_event(self, event):
        self.events.append(event)

    async def recall(self, query):

        return [
            e for e in self.events
            if query in str(e)
        ]