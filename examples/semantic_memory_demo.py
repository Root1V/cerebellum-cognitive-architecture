import asyncio
import logging
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.memory.semantic_memory import SemanticMemory

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("semantic_memory_demo")

class TeacherModule(CognitiveModule):
    """Módulo que simula a un profesor guardando conocimientos hechos."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("memory.available")
    
    async def teach_fact(self, key: str, definition: str):
        logger.info(f"🎓 Teaching fact: {key}")
        await self.publish("memory.store", {
            "scope": "semantic",
            "key": key,
            "value": definition
        })

    async def ask_question(self, key: str):
        logger.info(f"❓ Asking: What is {key}?")
        await self.publish("memory.recall", {
            "scope": "semantic",
            "key": key
        })

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "memory.available":
            found = message.payload.get("found")
            data = message.payload.get("data")
            if found:
                logger.info(f"✅ I remember! {data}")
            else:
                logger.info("❌ I don't know that yet.")

async def main():
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    sm = SemanticMemory()
    teacher = TeacherModule("teacher_lobe")

    runtime.register(sm)
    runtime.register(teacher)

    await runtime.start(run_id="demo-semantic")

    # 1. Guardar un hecho
    await teacher.teach_fact("Python", "Un lenguaje de programación interpretado y asíncrono.")
    await runtime.run_until_idle()

    # 2. Recuperarlo
    await teacher.ask_question("Python")
    await runtime.run_until_idle()

    # 3. Preguntar algo desconocido
    await teacher.ask_question("Java")
    await runtime.run_until_idle()

    await runtime.stop()

if __name__ == "__main__":
    asyncio.run(main())
