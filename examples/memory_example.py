# examples/working_memory_example.py
# Ejemplo de uso de la clase WorkingMemory

from cerebellum.cognition.memory.working_memory import WorkingMemory
from cerebellum.cognition.memory.episodic_memory import EpisodicMemory
from cerebellum.cognition.memory.manager import MemoryManager


import asyncio

async def working_example():
    wm = WorkingMemory()
    print("Memoria de trabajo inicial:", wm._state)

    # Agregar elementos
    for i in range(5):
        await wm.store(f"item_{i}", f"valor_{i}")
        print(f"Agregado item_{i}: {wm._state}")

    # Consultar un elemento
    val = await wm.retrieve("item_3")
    print("Valor de 'item_3':", val)

    # Actualizar varios elementos
    await wm.update({"item_4": "nuevo_valor_4", "item_5": "valor_5"})
    print("Estado tras update:", wm._state)

async def episodic_example():
    em = EpisodicMemory()
    print("Memoria episódica inicial:", em.events)

    # Almacenar eventos
    await em.store_event({"goal": "resolver problema", "result": "éxito", "timestamp": "2026-03-11"})
    await em.store_event({"goal": "leer documento", "result": "fallo", "timestamp": "2026-03-10"})
    print("Eventos almacenados:", em.events)

    # Recuperar eventos por query
    encontrados = await em.recall("éxito")
    print("Eventos con 'éxito':", encontrados)

    # Consultar los más recientes
    recientes = await em.recent(1)
    print("Evento más reciente:", recientes)

async def manager_example():
    mm = MemoryManager()
    print("Memoria de trabajo inicial:", mm.get_working()._state)
    print("Memoria episódica inicial:", mm.get_episodic().events)
    print("Memoria semántica inicial:", mm.get_semantic().knowledge)
    print("MemoryStream inicial:", mm.get_stream().memories)

    # Almacenar datos simples
    await mm.remember("item_simple", "valor_simple")
    print("WorkingMemory tras simple:", mm.get_working()._state)

    # Almacenar evento episódico
    evento = {"goal": "resolver problema", "result": "éxito", "timestamp": "2026-03-12"}
    await mm.remember("evento_1", evento)
    print("EpisodicMemory tras evento:", mm.get_episodic().events)

    # Almacenar hecho semántico
    hecho = {"fact": "París es capital de Francia", "definition": "Ciudad capital", "document": "wiki"}
    await mm.remember("hecho_1", hecho)
    print("SemanticMemory tras hecho:", mm.get_semantic().knowledge)

    # Almacenar evento stream
    stream_event = {"time": "2026-03-12T10:00", "data": "Sensor activado"}
    await mm.remember("stream_1", stream_event)
    print("MemoryStream tras evento:", mm.get_stream().memories)

    # Recuperar de cada memoria
    val_working = await mm.recall("item_simple", "working")
    val_episodic = await mm.recall("evento_1", "episodic")
    val_semantic = await mm.recall("hecho_1", "semantic")
    val_stream = await mm.recall("stream_1", "stream")
    print("Recall WorkingMemory:", val_working)
    print("Recall EpisodicMemory:", val_episodic)
    print("Recall SemanticMemory:", val_semantic)
    print("Recall MemoryStream:", val_stream)

    
if __name__ == "__main__":
    asyncio.run(working_example())
    asyncio.run(episodic_example())
    asyncio.run(manager_example())
