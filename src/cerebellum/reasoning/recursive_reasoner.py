# RLM Reasoning
#
# Estrategia: descomponer el problema en subproblemas hasta llegar
# a unidades simples que se pueden responder directamente.

from ..core.reasoning import Reasoner
from ..core.memory import Memory
from ..core.tool import Tool


class RecursiveReasoner(Reasoner):
    """
    Reasoner recursivo (RLM).
    Descompone problemas complejos en subproblemas hasta resolverlos.

    Subclases deben implementar:
        is_simple()  → ¿el problema es elemental?
        answer()     → resuelve un problema simple
        decompose()  → divide el problema en subproblemas
        combine()    → combina los resultados parciales
    """

    # ------------------------------------------------------------------
    # Interfaz pública de Reasoner
    # ------------------------------------------------------------------

    async def reason(self, context):
        """Punto de entrada simple: resuelve context como problema raíz."""
        return await self.solve(context)

    async def execute(
        self,
        plan: list[dict],
        memory: dict[str, Memory],
        tools: dict[str, Tool],
    ) -> list:
        """
        Ejecuta cada paso del plan como un subproblema independiente.
        """
        results = []
        for step in plan:
            result = await self.solve(step)
            results.append(result)
        return results

    # ------------------------------------------------------------------
    # Núcleo recursivo
    # ------------------------------------------------------------------

    async def solve(self, problem):
        if self.is_simple(problem):
            return await self.answer(problem)

        subproblems = self.decompose(problem)
        results = []
        for sp in subproblems:
            results.append(await self.solve(sp))

        return self.combine(results)

    # ------------------------------------------------------------------
    # Hooks para subclases
    # ------------------------------------------------------------------

    def is_simple(self, problem) -> bool:
        """Retorna True si el problema puede resolverse directamente."""
        return True

    async def answer(self, problem):
        """Resuelve un problema elemental."""
        return str(problem)

    def decompose(self, problem) -> list:
        """Divide el problema en subproblemas."""
        return [problem]

    def combine(self, results: list):
        """Combina los resultados parciales en una respuesta final."""
        return results