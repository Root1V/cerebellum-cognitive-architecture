# runtime/event_loop.py

import asyncio


class CognitiveEventLoop:

    def __init__(self, bus):
        self.bus = bus

    async def start(self):

        while True:
            await asyncio.sleep(0.01)