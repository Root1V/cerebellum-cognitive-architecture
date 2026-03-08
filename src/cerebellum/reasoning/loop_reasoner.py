# reasoning/loop_reasoner.py
#
# ReasoningLoop: en lugar de ejecutar pasos secuencialmente desde un plan fijo,
# itera sobre un ciclo   think → act → evaluate   hasta que el objetivo
# se cumpla o se alcance el límite de iteraciones.
#
# Diferencia clave con LLMReasoner / HierarchicalReasoner:
#   Secuencial  → El plan se genera una sola vez y cada paso se ejecuta en orden.
#   Loop        → En cada iteración el reasoner observa el estado actual
#                 (historial, resultado previo) y decide cuál es el siguiente
#                 paso, permitiendo corrección de curso y auto-evaluación.

from ..core.reasoning import Reasoner
from ..core.memory import Memory
from ..core.tool import Tool


class LoopReasoner(Reasoner):
    """
    Reasoning loop (ciclo de razonamiento).

    Ciclo por iteración
    -------------------
    1. _think  → decide el siguiente paso según el estado actual
    2. _act    → ejecuta ese paso (tools, LLM, …)
    3. _is_complete → evalúa si el objetivo ya fue alcanzado

    Si se alcanza max_iterations antes de completar el objetivo,
    devuelve el historial acumulado hasta ese momento.
    """

    def __init__(self, llm_client=None, max_iterations: int = 10):
        self.llm = llm_client
        self.max_iterations = max_iterations

    # ------------------------------------------------------------------
    # Interfaz pública de Reasoner
    # ------------------------------------------------------------------

    async def reason(self, context):
        """Punto de entrada simple: usa execute con memoria y tools vacíos."""
        return await self.execute(context, {}, [])

    async def execute(self, goal, memory: Memory, tools: dict[str, Tool]):
        """
        Ejecuta el ciclo de razonamiento.

        Parameters
        ----------
        goal   : el objetivo o plan que guía el razonamiento.
        memory : sistema de memoria disponible.
        tools  : herramientas disponibles (dict nombre→Tool o lista).
        """
        state = {
            "goal": goal,
            "history": [],
            "iteration": 0,
        }

        for i in range(self.max_iterations):
            state["iteration"] = i + 1

            # 1. Think — decidir el siguiente paso
            action = await self._think(state, memory, tools)

            # 2. Act — ejecutar la acción elegida
            result = await self._act(action, memory, tools)

            # Guardar en historial
            state["history"].append({
                "iteration": state["iteration"],
                "action": action,
                "result": result,
            })

            # 3. Evaluate — ¿ya terminamos?
            if await self._is_complete(state, result):
                break

        return state["history"]

    # ------------------------------------------------------------------
    # Núcleo del loop
    # ------------------------------------------------------------------

    async def _think(self, state: dict, memory: Memory, tools) -> dict | str:
        """
        Decide el siguiente paso basándose en el plan del planner y el historial.

        Si state["goal"] es una lista (plan estructurado del Planner), consume sus
        pasos en orden. Si es un dict/str (goal directo), usa actions por defecto.
        En una implementación con LLM real, aquí se construiría un prompt con el
        goal + historial y se le pediría al modelo la siguiente acción.
        """
        completed_actions = [
            h["action"].get("step") if isinstance(h["action"], dict) else h["action"]
            for h in state["history"]
        ]

        plan = state["goal"]

        if isinstance(plan, list):
            # Consume los pasos del plan en orden
            for plan_step in plan:
                action_name = plan_step.get("action") or plan_step.get("step")
                if action_name not in completed_actions:
                    return {"step": action_name, "meta": plan_step}
            return "done"

        # Fallback: sin plan estructurado, usar acciones por defecto
        available_actions = [
            "search_market_data",
            "analyze_trends",
            "generate_summary",
        ]
        remaining = [a for a in available_actions if a not in completed_actions]
        return {"step": remaining[0]} if remaining else "done"

    async def _act(self, action: dict | str, memory: Memory, tools) -> str | None:
        """
        Ejecuta la acción elegida por _think.

        tools puede ser un dict {nombre: Tool} o una lista.
        """
        if action == "done" or not isinstance(action, dict):
            return None

        step = action.get("step")

        if step == "search_market_data":
            tool = tools.get("web_search") if isinstance(tools, dict) else None
            if tool:
                return await tool.execute(query="AI market Latin America")
            return "Search results for AI market Latin America"

        if step == "analyze_trends":
            if self.llm:
                return await self.llm.complete(
                    f"Analyze AI adoption trends. Context: {action}"
                )
            return "AI adoption growing in fintech and healthcare"

        if step == "generate_summary":
            return "AI market in LATAM shows strong growth potential"

        return f"unknown action: {step}"

    async def _is_complete(self, state: dict, last_result) -> bool:
        """
        Condición de parada del loop.

        El objetivo se considera alcanzado cuando:
        - se ejecutó 'generate_summary', o
        - la última acción fue 'done' (last_result is None)
        """
        if last_result is None:
            return True

        actions_done = [
            h["action"].get("step") if isinstance(h["action"], dict) else h["action"]
            for h in state["history"]
        ]
        return "generate_summary" in actions_done
