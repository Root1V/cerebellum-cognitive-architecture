from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel, Field

from ..core.models import Fact
from .symbolic import RuleEngine


class Condition(BaseModel):
    fact_kind: str                           = Field(description="The 'kind' of the fact to match against.")
    fact_name: str                           = Field(description="The 'name' of the fact to match against.")
    op:        Literal["==", "!=", ">", ">=", "<", "<=", "in", "not_in", "contains"] = Field(
        default="==", description="Comparison operator to apply. Use 'contains' to check if a string fact value contains a substring."
    )
    value:     Any                           = Field(description="The value to compare the fact against.")


class Rule(BaseModel):
    name:       str             = Field(description="Unique identifier for this rule, e.g. 'high_confidence_query'.")
    when:       List[Condition] = Field(description="All conditions that must hold for the rule to fire.")
    then_facts: List[Dict[str, Any]] = Field(description="Facts to derive when all conditions are met.")


def _coerce(fact_value: Any, expected: Any) -> Any:
    """Cast expected to the same type as fact_value when the LLM returns numbers as strings."""
    if fact_value is None:
        return expected
    try:
        return type(fact_value)(expected)
    except (ValueError, TypeError):
        return expected


def _matches(fact_value: Any, op: str, expected: Any) -> bool:
    if fact_value is None:
        return False
    if op not in ("in", "not_in", "contains"):
        expected = _coerce(fact_value, expected)
    if op == "==":       return fact_value == expected
    if op == "!=":       return fact_value != expected
    if op == ">":        return fact_value > expected
    if op == ">=":       return fact_value >= expected
    if op == "<":        return fact_value < expected
    if op == "<=":       return fact_value <= expected
    if op == "in":       return fact_value in expected        # fact is a member of a collection
    if op == "not_in":   return fact_value not in expected
    if op == "contains": return expected in fact_value        # fact string contains a substring
    return False


class DeclarativeRuleEngine(RuleEngine):

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    def derive(self, facts: List[Fact]) -> List[Fact]:
        # Index by (kind, name) to avoid collisions between facts with same name
        fact_index: Dict[tuple, Any] = {(f.kind, f.name): f.value for f in facts}
        derived: List[Fact] = []

        for rule in self.rules:
            if all(
                _matches(fact_index.get((c.fact_kind, c.fact_name)), c.op, c.value)
                for c in rule.when
            ):
                for item in rule.then_facts:
                    derived.append(Fact(**item))

        return derived

