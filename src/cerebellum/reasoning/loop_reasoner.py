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
from ..core.llm import LLMClient
from ..planners import Plan


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

    def __init__(self, llm_client: LLMClient | None = None, max_iterations: int = 10):
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
        Decide el siguiente paso consumiendo el plan del Planner en orden.

        El Planner es responsable de determinar QUÉ pasos ejecutar.
        El Reasoner es responsable de ITERAR sobre ellos observando el
        historial acumulado — eso es lo que diferencia ReAct de ejecución
        secuencial simple.

        En una implementación con LLM real, aquí se construiría un prompt
        con goal + historial para que el modelo decida el siguiente paso,
        en lugar de consumir el plan linealmente.
        """
        completed_actions = [
            h["action"].get("step") if isinstance(h["action"], dict) else h["action"]
            for h in state["history"]
        ]

        plan = state["goal"]

        if isinstance(plan, Plan):
            for plan_step in plan.steps:
                if plan_step.action not in completed_actions:
                    return {"step": plan_step.action, "meta": plan_step}

        # Plan agotado o no estructurado — el loop termina
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
            return await self.llm.think(
                prompt=f"Execute step '{step}'. Step data: {meta}",
                context="You are a reasoning assistant operating in a ReAct loop. Execute the step and return an observation.",
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
        - last_result es None (_think() señaló "done" → _invoke() devolvió None), o
        - todos los pasos del plan fueron completados (segundo chequeo de seguridad).
        """
        if last_result is None:
            return True

        completed = {
            h["action"].get("step") if isinstance(h["action"], dict) else h["action"]
            for h in state["history"]
        }

        plan = state["goal"]
        if isinstance(plan, Plan):
            plan_steps = {step.action for step in plan.steps}
            return plan_steps.issubset(completed)

        return True
