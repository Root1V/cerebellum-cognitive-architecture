# symbolic.py
#
# Foundation of the symbolic layer.
#
# Contains:
#  - Abstract base classes: RuleEngine, ConstraintEngine
#  - Shared primitives: Condition, build_fact_index, _coerce, _matches
#
# Both DeclarativeRuleEngine and DeclarativeConstraintEngine import from here
# so the matching logic lives in exactly one place.

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field

from ..core.models import ConstraintViolation, Fact


# ─────────────────────────────────────────────────────────────
# Shared primitive: Condition
# ─────────────────────────────────────────────────────────────

class Condition(BaseModel):
    fact_kind: str = Field(description="The 'kind' of the fact to match against.")
    fact_name: str = Field(description="The 'name' of the fact to match against.")
    op: Literal["==", "!=", ">", ">=", "<", "<=", "in", "not_in", "contains"] = Field(
        default="==",
        description=(
            "Comparison operator. Use 'contains' to check if a string fact contains "
            "a substring; 'in' to check if a fact value belongs to a collection."
        ),
    )
    value: Any = Field(description="The value to compare the fact against.")


# ─────────────────────────────────────────────────────────────
# Shared primitive: fact index
# ─────────────────────────────────────────────────────────────

def build_fact_index(facts: List[Fact]) -> Dict[tuple, Any]:
    """Index facts by (kind, name) to avoid collisions between facts with the same name."""
    return {(f.kind, f.name): f.value for f in facts}


# ─────────────────────────────────────────────────────────────
# Shared primitive: matching
# ─────────────────────────────────────────────────────────────

def _coerce(fact_value: Any, expected: Any) -> Any:
    """Cast expected to the same type as fact_value.
    Handles the common case where the LLM returns a numeric threshold as a string.
    """
    if fact_value is None:
        return expected
    try:
        return type(fact_value)(expected)
    except (ValueError, TypeError):
        return expected


def _matches(fact_value: Any, op: str, expected: Any) -> bool:
    """Evaluate a single condition against a fact value."""
    if fact_value is None:
        return False
    if op not in ("in", "not_in", "contains"):
        expected = _coerce(fact_value, expected)
    if op == "==":
        return fact_value == expected
    if op == "!=":
        return fact_value != expected
    if op == ">":
        return fact_value > expected
    if op == ">=":
        return fact_value >= expected
    if op == "<":
        return fact_value < expected
    if op == "<=":
        return fact_value <= expected
    if op == "in":
        return fact_value in expected        # fact is a member of a collection
    if op == "not_in":
        return fact_value not in expected
    if op == "contains":
        return expected in fact_value        # fact string contains a substring
    return False


# ─────────────────────────────────────────────────────────────
# Abstract base classes
# ─────────────────────────────────────────────────────────────

class RuleEngine(ABC):
    @abstractmethod
    def derive(self, facts: List[Fact]) -> List[Fact]:
        raise NotImplementedError


class ConstraintEngine(ABC):
    @abstractmethod
    def validate(self, facts: List[Fact]) -> List[ConstraintViolation]:
        raise NotImplementedError
