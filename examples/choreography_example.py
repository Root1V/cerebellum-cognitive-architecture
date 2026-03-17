import asyncio
import logging
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("choreography_example")

class PerceptionModule(CognitiveModule):
    """Simula la entrada de datos sensoriales."""
    async def perceive(self, text: str):
        logger.info(f"Perceived: {text}")
        await self.publish("perception.text", {"text": text})

class MemoryModule(CognitiveModule):
    """Módulo de memoria que reacciona a percepciones."""
    def __init__(self, name: str):
        super().__init__(name)
        self.storage = []

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "perception.text":
            text = message.payload.get("text")
            logger.info(f"Memory module storing: {text}")
            self.storage.append(text)
            # Avisamos que la memoria ha sido actualizada
            await self.publish("memory.updated", {"count": len(self.storage)})

class ReasoningModule(CognitiveModule):
    """Módulo que reacciona a actualizaciones de memoria."""
    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "memory.updated":
            count = message.payload.get("count")
            logger.info(f"Reasoning: I now have {count} items in memory. Should I act?")
            if count >= 3:
                await self.publish("reasoning.decision", {"action": "stop_perceiving"})

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Registrar módulos
    perceiver = PerceptionModule("perceiver")
    memory = MemoryModule("memory")
    reasoner = ReasoningModule("reasoner")

    runtime.register(perceiver)
    runtime.register(memory)
    runtime.register(reasoner)

    # Iniciar runtime
    await runtime.start(run_id="choreography-demo")

    # Simular una ráfaga de percepciones
    for i in range(5):
        await perceiver.perceive(f"Input {i}")
        # Procesamos lo que haya en el bus después de cada entrada
        await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
