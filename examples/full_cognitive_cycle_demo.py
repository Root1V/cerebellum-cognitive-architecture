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

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("full_demo")

class UserLobe(CognitiveModule):
    """Módulo que representa al usuario, inicia estímulos y recibe reportes de ejecución."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("action.completed")
    
    async def request_action(self, text: str):
        msg_id = str(uuid.uuid4())
        logger.info(f"🌍 [USER] Emitting stimulus: '{text}' (ID={msg_id})")
        await self.publish("perception.process", {
            "input_type": "text",
            "raw_data": text
        }, correlation_id=msg_id)

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "action.completed":
            success = message.payload.get("success")
            goal = message.payload.get("metadata", {}).get("goal")
            logger.info(f"🎯 [USER] Received execution report for: '{goal}'")
            if success:
                logger.info("   ✅ CONGRATULATIONS: Cognitive cycle COMPLETED and SUCCESSFUL.")
            else:
                logger.error("   ❌ WARNING: Action failed during execution.")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Inicializamos todos los lóbulos del cerebro
    perception = TextPerceptionModule()
    # 2. Atención (Filtro) - Foco en algo muy relacionado
    attention = SimpleAttentionModule(initial_focus="investigación de micro-servicios y arquitectura")
    reasoning = LLMPlannerModule()
    action = MotorCortexModule()
    user = UserLobe("user_lobe")

    # Registro de módulos
    runtime.register(perception)
    runtime.register(attention)
    runtime.register(reasoning)
    runtime.register(action)
    runtime.register(user)

    await runtime.start(run_id="demo-full-cycle")

    # Simulamos el estímulo inicial
    await user.request_action("Investiga sobre la arquitectura de micro-servicios asíncronos")
    
    # Dejamos que toda la cadena coreografiada ocurra:
    # Sensor (User) -> Perception -> Attention -> Reasoning -> Action -> User (Report)
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
