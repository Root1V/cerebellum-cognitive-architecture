import asyncio
import logging
import uuid
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.planners.llm_planner import LLMPlannerModule
from cerebellum.cognition.attention.simple_attention import SimpleAttentionModule
from cerebellum.cognition.perception.text_perception import TextPerceptionModule

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("reasoning_demo")

class MotorCortexMock(CognitiveModule):
    """Módulo que simula a la corteza motora recibiendo el plan para ejecutar."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("reasoning.plan_ready")
    
    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "reasoning.plan_ready":
            plan = message.payload.get("plan", {})
            steps = plan.get("steps", [])
            logger.info("🤖 MOTOR CORTEX: Received plan for execution!")
            for s in steps:
                logger.info(f"   [Step {s.get('step')}] Action: {s.get('action')} - Goal: {s.get('goal')}")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Inicializamos la cadena completa
    # 1. Percepción (Ojos)
    perception = TextPerceptionModule()
    # 2. Atención (Filtro) - Foco en 'tareas'
    attention = SimpleAttentionModule(initial_focus="tareas y recordatorios")
    # 3. Razonamiento (Cerebro)
    reasoning = LLMPlannerModule()
    # 4. Acción (Músculos - Mock)
    motor = MotorCortexMock("motor_lobe")

    runtime.register(perception)
    runtime.register(attention)
    runtime.register(reasoning)
    runtime.register(motor)

    await runtime.start(run_id="demo-reasoning-choreography")

    # Escenario: Entrada de alta relevancia respecto al foco
    msg_id = str(uuid.uuid4())
    logger.info(f"🌍 STIMULUS (ID={msg_id}): 'Recordatorio: comprar pan al salir del trabajo'")
    await runtime.publish(Message(
        id=msg_id,
        sender="environment",
        receiver="broadcast",
        topic="perception.process",
        payload={"input_type": "text", "raw_data": "Recordatorio: comprar pan al salir del trabajo"}
    ))

    # Dejamos que la cadena (Perception -> Attention -> Reasoning -> Motor) ocurra
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
