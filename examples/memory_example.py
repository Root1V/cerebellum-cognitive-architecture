# examples/working_memory_example.py
# Ejemplo de uso de la clase WorkingMemory

from cerebellum.cognition.memory.working_memory import WorkingMemory
from cerebellum.cognition.memory.episodic_memory import EpisodicMemory


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

    
if __name__ == "__main__":
    asyncio.run(working_example())
    asyncio.run(episodic_example())


# WorkingMemory (memoria de trabajo): almacena información temporal y actual, útil para tareas en curso, cálculos o contexto inmediato. Es como una “RAM” cognitiva: rápido acceso, datos volátiles, se usa para manipular información activa.

# EpisodicMemory (memoria episódica): guarda experiencias pasadas, eventos, acciones y resultados. Es como un “diario” cognitivo: registra lo que ocurrió, cuándo y cómo, permitiendo recordar y analizar experiencias previas.

# Agregado item_1: {'item_0': 'valor_0', 'item_1': 'valor_1'}
# Agregado item_2: {'item_0': 'valor_0', 'item_1': 'valor_1', 'item_2': 'valor_2'}
# Agregado item_3: {'item_0': 'valor_0', 'item_1': 'valor_1', 'item_2': 'valor_2', 'item_3': 'valor_3'}
# Agregado item_4: {'item_0': 'valor_0', 'item_1': 'valor_1', 'item_2': 'valor_2', 'item_3': 'valor_3', 'item_4': 'valor_4'}
# Valor de 'item_3': valor_3
# Estado tras update: {'item_0': 'valor_0', 'item_1': 'valor_1', 'item_2': 'valor_2', 'item_3': 'valor_3', 'item_4': 'nuevo_valor_4', 'item_5': 'valor_5'}
# Memoria episódica inicial: []
# Eventos almacenados: [{'goal': 'resolver problema', 'result': 'éxito', 'timestamp': '2026-03-11'}, {'goal': 'leer documento', 'result': 'fallo', 'timestamp': '2026-03-10'}]
# Eventos con 'éxito': [{'goal': 'resolver problema', 'result': 'éxito', 'timestamp': '2026-03-11'}]
# Evento más reciente: [{'goal': 'leer documento', 'result': 'fallo', 'timestamp': '2026-03-10'}]
