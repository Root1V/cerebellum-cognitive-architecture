# memory/memory_stream.py

class MemoryStream:

    def __init__(self):
        self.memories = []

    async def add(self, event):

        self.memories.append({
            "timestamp": event["time"],
            "data": event["data"]
        })

    async def recent(self, n=10):

        return self.memories[-n:]