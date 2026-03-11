from typing import List, Literal

from pydantic import BaseModel, Field

from ..core.models import ConstraintViolation, Fact
from .symbolic import Condition, ConstraintEngine, _matches, build_fact_index


class Constraint(BaseModel):
    name:     str                               = Field(description="Identifier for this constraint, e.g. 'max_budget_exceeded'.")
    message:  str                               = Field(description="Human-readable explanation shown when the constraint is violated.")
    severity: Literal["low", "medium", "high"]  = Field(default="medium", description="Impact level of the violation.")
    when:     List[Condition]                   = Field(description="All conditions that must hold for the constraint to be considered violated.")


class DeclarativeConstraintEngine(ConstraintEngine):

    def __init__(self, constraints: List[Constraint]) -> None:
        self.constraints = constraints

    def validate(self, facts: List[Fact]) -> List[ConstraintViolation]:
        fact_index = build_fact_index(facts)
        violations: List[ConstraintViolation] = []

        for constraint in self.constraints:
            if all(
                _matches(fact_index.get((c.fact_kind, c.fact_name)), c.op, c.value)
                for c in constraint.when
            ):
                violations.append(
                    ConstraintViolation(
                        name=constraint.name,
                        message=constraint.message,
                        severity=constraint.severity,
                    )
                )

        return violations
