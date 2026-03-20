import asyncio
import logging
import uuid
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.perception.text_perception import TextPerceptionModule
from cerebellum.cognition.attention.simple_attention import SimpleAttentionModule
from cerebellum.cognition.planners.llm_planner import LLMPlannerModule
from cerebellum.cognition.action.motor_cortex import MotorCortexModule
from cerebellum.cognition.learning.simple_learning import LearningModule

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("learning_demo")

class FullCycleManager(CognitiveModule):
    """Monitorea el ciclo completo y muestra los insights de aprendizaje."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("learning.updated")
    
    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "learning.updated":
            insights = message.payload.get("insights", {})
            goal = message.payload.get("metadata", {}).get("goal")
            logger.info("🎓 LEARNING LOBE UPDATED:")
            logger.info(f"   - Task: '{goal}'")
            logger.info(f"   - Total Experiences: {insights.get('total')}")
            logger.info(f"   - Success Rate: {insights.get('success_rate'):.2%}")
            logger.info(f"   - System Trend: {insights.get('trend')}")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # 1. Componentes del sistema
    perception = TextPerceptionModule()
    attention = SimpleAttentionModule(initial_focus="tareas críticas")
    reasoning = LLMPlannerModule()
    action = MotorCortexModule()
    learning = LearningModule()
    manager = FullCycleManager("monitor_lobe")

    # 2. Registro
    runtime.register(perception)
    runtime.register(attention)
    runtime.register(reasoning)
    runtime.register(action)
    runtime.register(learning)
    runtime.register(manager)

    await runtime.start(run_id="demo-learning-choreography")

    # ESTÍMULO 1: Éxito
    msg_id = str(uuid.uuid4())
    logger.info("🌍 [STIMULUS 1]: 'Actualizar reporte trimestral'")
    await runtime.publish(Message(
        id=msg_id,
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "Actualizar reporte trimestral"}
    ))
    await runtime.run_until_idle()

    # ESTÍMULO 2: Otro éxito
    msg_id2 = str(uuid.uuid4())
    logger.info("🌍 [STIMULUS 2]: 'Enviar correos pendientes'")
    await runtime.publish(Message(
        id=msg_id2,
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "Enviar correos pendientes"}
    ))
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
