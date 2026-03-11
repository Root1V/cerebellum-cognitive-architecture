from typing import Any, Dict, List

from pydantic import BaseModel, Field

from ..core.models import Fact
from .symbolic import Condition, RuleEngine, _matches, build_fact_index


class Rule(BaseModel):
    name:       str              = Field(description="Unique identifier for this rule, e.g. 'high_confidence_query'.")
    when:       List[Condition]  = Field(description="All conditions that must hold for the rule to fire.")
    then_facts: List[Dict[str, Any]] = Field(description="Facts to derive when all conditions are met.")


class DeclarativeRuleEngine(RuleEngine):

    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules

    def derive(self, facts: List[Fact]) -> List[Fact]:
        fact_index = build_fact_index(facts)
        derived: List[Fact] = []

        for rule in self.rules:
            if all(
                _matches(fact_index.get((c.fact_kind, c.fact_name)), c.op, c.value)
                for c in rule.when
            ):
                for item in rule.then_facts:
                    derived.append(Fact(**item))

        return derived

