import asyncio
import logging
import uuid
from cerebellum.cognition.runtime.event_bus import MessageBus
from cerebellum.cognition.runtime.cognitive_runtime import CognitiveRuntime, CognitiveModule
from cerebellum.cognition.runtime.types import Message, CognitiveContext
from cerebellum.cognition.memory.episodic_memory import EpisodicMemory

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("episodic_memory_demo")

class UserLobe(CognitiveModule):
    """Módulo que simula interacción con la memoria episódica."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.subscriptions.append("memory.available")
        self.subscriptions.append("memory.stored")
    
    async def save_experience(self, content: str, mood: str):
        logger.info(f"💾 Saving experience: {content} (Mood: {mood})")
        await self.publish("memory.store", {
            "scope": "episodic",
            "key": str(uuid.uuid4()),
            "value": {
                "content": content,
                "mood": mood,
                "type": "experience"
            }
        })

    async def search_memories(self, query: str):
        logger.info(f"🏮 Searching memories for: '{query}'")
        await self.publish("memory.search", {
            "query": query,
            "limit": 2
        })

    async def on_message(self, message: Message, context: CognitiveContext) -> None:
        if message.topic == "memory.available":
            data = message.payload.get("data")
            meta = message.payload.get("metadata", {})
            logger.info(f"✅ Search Results for '{meta.get('search_query')}':")
            if isinstance(data, list):
                for i, res in enumerate(data):
                    logger.info(f"  [{i+1}] Score: {res['score']:.4f} - Data: {res['payload']['content']}")
            else:
                logger.info(f"  Data: {data}")
        
        elif message.topic == "memory.stored":
            logger.info(f"📥 Acknowledged: Entry stored in {message.payload.get('scope')}")

async def main():
    # NOTA: Asegúrate de tener Qdrant corriendo en localhost:6333 
    # o este demo fallará al intentar conectar.
    bus = MessageBus()
    runtime = CognitiveRuntime(bus)

    # Inicializamos EpMemory con los componentes reales
    # Si falla la conexión, se verá en los logs
    try:
        em = EpisodicMemory()
        user = UserLobe("user_lobe")

        runtime.register(em)
        runtime.register(user)

        await runtime.start(run_id="demo-episodic")

        # 1. Guardamos experiencias variadas
        await user.save_experience("Hoy aprendí a volar un dron en el parque.", "excited")
        await user.save_experience("El café de la mañana estaba demasiado amargo.", "annoyed")
        await user.save_experience("He terminado de implementar la arquitectura cognitiva.", "proud")
        
        # Procesamos el guardado
        await runtime.run_until_idle()

        # 2. Buscamos por concepto (no por palabras exactas)
        # Debería encontrar el del dron
        await user.search_memories("actividades al aire libre con tecnología")
        await runtime.run_until_idle()

        # Debería encontrar el de la arquitectura
        await user.search_memories("progreso en el desarrollo del proyecto")
        await runtime.run_until_idle()

        await runtime.stop()
    except Exception as e:
        logger.error(f"Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
