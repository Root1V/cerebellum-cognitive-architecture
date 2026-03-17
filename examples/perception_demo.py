import asyncio
import logging
import uuid
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.perception.text_perception import TextPerceptionModule

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("perception_demo")

class AttentionMock(CognitiveModule):
    """Módulo que simula el lóbulo de atención recibiendo percepciones."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("perception.output")
    
    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "perception.output":
            result = message.payload.get("result", {})
            normalized = result.get("normalized", {})
            logger.info("🧠 Attention received new perception:")
            logger.info(f"   - Raw: {result.get('raw')}")
            logger.info(f"   - Stats: {normalized.get('num_words')} words, {normalized.get('length')} characters")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Inicializamos módulos
    perception = TextPerceptionModule()
    attention = AttentionMock("attention_lobe")

    runtime.register(perception)
    runtime.register(attention)

    await runtime.start(run_id="demo-perception")

    # 1. Simulamos una entrada del mundo exterior
    logger.info("🌍 External Stimulus: 'Hola Cerebellum, ¿cómo estás hoy?'")
    await runtime.publish(Message(
        id=str(uuid.uuid4()),
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={
            "input_type": "text",
            "raw_data": "Hola Cerebellum, ¿cómo estás hoy?"
        }
    ))

    # Dejamos que el sistema procese la coreografía
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
