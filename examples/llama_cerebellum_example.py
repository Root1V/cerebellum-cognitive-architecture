"""
Ejemplo: LlamaAdapter (axonium-sdk) + cerebellum-architecture

Muestra cómo conectar el LLM local con los componentes cognitivos.

Variables de entorno requeridas (archivo .env):
    LLM_BASE_URL=http://localhost:8080
    LLM_USERNAME=tu_usuario
    LLM_PASSWORD=tu_contraseña
"""
import asyncio
from cerebellum.llm import LlamaAdapter
from cerebellum.planners import LLMPlanner
from cerebellum.reasoning import LLMReasoner


async def main():
    # 1. Crear el adapter LLM local usando axonium
    llm = LlamaAdapter(
        model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf",
        timeout=60.0,
        system_prompt="Eres un asistente de planificación estratégica.",
    )

    # 2. Planner LLM: genera un plan a partir del goal
    planner = LLMPlanner(llm_client=llm)
    plan = await planner.create_plan(
        goal="Analizar el mercado de IA en LATAM para 2026"
    )
    print("=== Plan generado ===")
    print(plan)

    # 3. Reasoner LLM: ejecuta razonamiento con el LLM
    reasoner = LLMReasoner(llm_client=llm)

    step = {"action": "analyze_trends", "goal": "IA en LATAM 2026"}
    result = await reasoner.solve(step=step, memory={}, tools={})
    print("\n=== Resultado del razonamiento ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
