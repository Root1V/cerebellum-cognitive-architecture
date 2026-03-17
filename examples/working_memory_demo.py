import asyncio
import logging
import uuid
from typing import Any
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.memory.working_memory import WorkingMemory

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("working_memory_demo")

class UserModule(CognitiveModule):
    """Módulo que simula a un usuario pidiendo guardar y recuperar cosas."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("memory.available")
    
    async def request_store(self, key: str, value: Any):
        logger.info(f"Requesting to store: {key} = {value}")
        await self.publish("memory.store", {
            "scope": "working",
            "key": key,
            "value": value
        })

    async def request_recall(self, key: str):
        logger.info(f"Requesting to recall: {key}")
        # Guardamos el ID para identificar la respuesta
        msg_id = str(uuid.uuid4())
        message = Message(
            id=msg_id,
            sender=self.name,
            receiver="broadcast",
            topic="memory.recall",
            payload={"scope": "working", "key": key}
        )
        await self._runtime.publish(message)
        return msg_id

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "memory.available":
            found = message.payload.get("found")
            data = message.payload.get("data")
            orig_id = message.payload.get("id")
            logger.info(f"Received recall result (orig_id={orig_id}): Found={found}, Data={data}")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Inicializamos módulos
    wm = WorkingMemory() # Se registra como 'memory.working' por defecto
    user = UserModule("user_lobe")

    runtime.register(wm)
    runtime.register(user)

    await runtime.start(run_id="demo-working-memory")

    # 1. Pedimos guardar algo
    await user.request_store("username", "Antigravity")
    await runtime.run_until_idle()

    # 2. Pedimos recuperarlo
    await user.request_recall("username")
    await runtime.run_until_idle()

    # 3. Pedimos algo que no existe
    await user.request_recall("non_existent_key")
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
