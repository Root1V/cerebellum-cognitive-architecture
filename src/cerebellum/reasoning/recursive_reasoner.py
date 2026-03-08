# RLM Reasoning


from ..core.reasoning import Reasoner


class RecursiveReasoner(Reasoner):

    async def solve(self, problem):

        if self.is_simple(problem):
            return await self.answer(problem)

        subproblems = self.decompose(problem)

        results = []

        for sp in subproblems:

            results.append(
                await self.solve(sp)
            )

        return self.combine(results) 