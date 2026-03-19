import asyncio
import logging
import uuid
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.attention.simple_attention import SimpleAttentionModule
from cerebellum.cognition.perception.text_perception import TextPerceptionModule

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("attention_demo")

class PlanningMock(CognitiveModule):
    """Módulo que simula al planificador recibiendo atención enfocada."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("attention.focused")
    
    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "attention.focused":
            focused = message.payload.get("focused_result", {})
            score = message.payload.get("relevance_score")
            meta = message.payload.get("metadata", {})
            logger.info(f"🎯 Planning received ATENTION FOCUS (Focus query: '{meta.get('focus')}'):")
            logger.info(f"   - Relevance Score: {score:.4f}")
            logger.info(f"   - Content: {focused.get('raw')[:50]}...")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # 1. Cargamos el lóbulo de atención con un foco inicial: "alimentos"
    attention = SimpleAttentionModule(initial_focus="comida y restaurantes")
    perception = TextPerceptionModule()
    planner = PlanningMock("planning_lobe")

    runtime.register(perception)
    runtime.register(attention)
    runtime.register(planner)

    await runtime.start(run_id="demo-attention-smart")

    # 2. Enviamos una percepción sobre algo que NO es comida
    logger.info("🌍 [Stimulus 1]: 'El mercado bursátil está subiendo un 2%'")
    await runtime.publish(Message(
        id=str(uuid.uuid4()),
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "El mercado bursátil está subiendo un 2%"}
    ))
    await runtime.run_until_idle()

    # 3. Enviamos una percepción sobre algo que SÍ es comida
    logger.info("🌍 [Stimulus 2]: 'He encontrado un excelente restaurante de sushi cerca'")
    await runtime.publish(Message(
        id=str(uuid.uuid4()),
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "He encontrado un excelente restaurante de sushi cerca"}
    ))
    await runtime.run_until_idle()

    # 4. Actualizamos el foco de atención DINÁMICAMENTE
    logger.info("💡 UPDATING ATTENTION FOCUS: 'finanzas y tecnología'")
    await runtime.publish(Message(
        id=str(uuid.uuid4()),
        sender="user",
        receiver="broadcast",
        topic="attention.set_focus",
        payload={"query": "finanzas y tecnología"}
    ))
    await runtime.run_until_idle()

    # 5. Re-enviamos el primer estímulo de bolsa para ver si el score mejoró
    logger.info("🌍 [Repeat Stimulus 1]: 'El mercado bursátil está subiendo un 2%'")
    await runtime.publish(Message(
        id=str(uuid.uuid4()),
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "El mercado bursátil está subiendo un 2%"}
    ))
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
