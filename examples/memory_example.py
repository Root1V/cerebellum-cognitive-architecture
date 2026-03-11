# examples/working_memory_example.py
# Ejemplo de uso de la clase WorkingMemory

from cerebellum.cognition.memory.working_memory import WorkingMemory


import asyncio

async def main():
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

    # Limpiar memoria (simulado)
    wm._state.clear()
    print("Memoria después de limpiar:", wm._state)

if __name__ == "__main__":
    asyncio.run(main())
