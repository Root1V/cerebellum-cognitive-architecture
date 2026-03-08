# reasoning/loop_reasoner.py
#
# Implementa el patrón ReAct: Reason + Act en un loop.
#
# Distinción clave respecto a otros componentes del sistema:
#
#   Action.execute()      → efecto AMBIENTAL: imprime, escribe, llama API externa.
#                           Se ejecuta DESPUÉS del razonamiento en CognitiveSystem.
#
#   _invoke() aquí        → uso COGNITIVO de tools: recopila datos que alimentan
#                           la siguiente decisión. El resultado de la iteración N
#                           informa _think() en la iteración N+1. Sin esta
#                           retroalimentación el loop perdería su razón de existir.
#
#   controller.is_goal_satisfied() → ¿debo reiniciar el ciclo cognitivo completo?
#   _loop_satisfied()     → ¿debo continuar iterando dentro de esta sesión de
#                           razonamiento? Concerns distintos, niveles distintos.
#
# Diferencia con LLMReasoner / HierarchicalReasoner:
#   Secuencial → el plan se genera una sola vez y cada paso se ejecuta en orden.
#   Loop (ReAct) → en cada iteración el reasoner observa el estado acumulado
#                  (historial + resultado previo) y decide el siguiente paso,
#                  permitiendo corrección de curso y auto-evaluación.

from ..core.reasoning import Reasoner
from ..core.memory import Memory
from ..core.tool import Tool


class LoopReasoner(Reasoner):
    """
    Reasoner que implementa el patrón ReAct (Reason + Act).

    Ciclo por iteración
    -------------------
    1. _think()          → decide el siguiente paso observando el estado acumulado
    2. _invoke()         → usa una tool cognitivamente para obtener datos
    3. _loop_satisfied() → evalúa si este loop de razonamiento concluyó

    Nota: _invoke() NO es Action.execute() — su propósito es recopilar
    información que alimenta la próxima iteración de _think(), no producir
    efectos ambientales. El efecto ambiental ocurre en CognitiveSystem paso 6.5.

    Si se alcanza max_iterations antes de satisfacer el loop,
    devuelve el historial acumulado hasta ese momento.
    """

    def __init__(self, llm_client=None, max_iterations: int = 10):
        self.llm = llm_client
        self.max_iterations = max_iterations

    # ------------------------------------------------------------------
    # Interfaz pública de Reasoner
    # ------------------------------------------------------------------

    async def execute(
        self,
        goal,
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
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

            # 2. Invoke — usar tool cognitivamente para obtener datos
            result = await self._invoke(action, memory, tools)

            # Guardar en historial
            state["history"].append({
                "iteration": state["iteration"],
                "action": action,
                "result": result,
            })

            # 3. Loop satisfied — ¿terminamos esta sesión de razonamiento?
            if await self._loop_satisfied(state, result, tools):
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

        # Fallback: sin plan estructurado — derivar pasos de las tools registradas.
        # Esto hace al reasoner agnóstico al dominio: no importa qué tools estén
        # disponibles, las itera en orden hasta agotarlas.
        if isinstance(tools, dict) and tools:
            remaining = [name for name in tools if name not in completed_actions]
            return {"step": remaining[0]} if remaining else "done"

        # Sin plan ni tools — nada que ejecutar
        return "done"

    async def _invoke(self, action: dict | str, memory: Memory, tools) -> str | None:
        """
        Uso COGNITIVO de tools: recopila datos que alimentan la próxima iteración.

        Esto NO es Action.execute(). No produce efectos ambientales.
        El resultado se almacena en el historial y alimenta _think() en N+1.

        Orden de delegación:
          1. Tool registrada cuyo nombre coincide con el paso.
          2. LLM, si está configurado — genera una observación sobre el paso.
          3. Placeholder genérico (útil en tests / sin infraestructura real).
        """
        if action == "done" or not isinstance(action, dict):
            return None

        step = action.get("step")
        meta = action.get("meta", {})

        # 1. Delegar a tool registrada
        tool = tools.get(step) if isinstance(tools, dict) else None
        if tool:
            return await tool.execute()

        # 2. Delegar al LLM
        if self.llm:
            return await self.llm.complete(
                f"Execute step '{step}'. Context: {meta}"
            )

        # 3. Placeholder — sin tool ni LLM (suficiente para tests unitarios)
        return f"executed: {step}"

    async def _loop_satisfied(self, state: dict, last_result, tools) -> bool:
        """
        Condición de parada del loop de razonamiento (ReAct interno).

        Responde: ¿debo continuar iterando dentro de esta sesión?
        NO es controller.is_goal_satisfied(), que responde: ¿debo reiniciar
        el ciclo cognitivo completo? Ambos existen en niveles distintos.

        El loop se considera satisfecho cuando:
        - last_result es None (la invocación indicó 'done'), o
        - todos los pasos del plan fueron completados, o
        - (sin plan) todas las tools registradas fueron invocadas.
        """
        if last_result is None:
            return True

        completed = {
            h["action"].get("step") if isinstance(h["action"], dict) else h["action"]
            for h in state["history"]
        }

        plan = state["goal"]
        if isinstance(plan, list):
            plan_steps = {step.get("action") or step.get("step") for step in plan}
            return plan_steps.issubset(completed)

        # Fallback sin plan: completo cuando todas las tools disponibles fueron llamadas
        if isinstance(tools, dict) and tools:
            return set(tools.keys()).issubset(completed)

        return True
