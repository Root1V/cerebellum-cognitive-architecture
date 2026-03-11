# symbolic/compiler.py
#
# Compiladores simbólicos: traducen lenguaje natural → modelos Pydantic tipados.
#
# Diseño:
#   LLMSymbolicCompiler[T]  — base genérica con la lógica compartida
#   LLMRuleCompiler         — compila Rule  (subclase, solo define prompt y modelo)
#   LLMConstraintCompiler   — compila Constraint (ídem)
#
# Para agregar un nuevo tipo de compilador (e.g. LLMPlanCompiler) basta con:
#   1. Subclasificar LLMSymbolicCompiler[MiModelo]
#   2. Definir _system_prompt y _output_model
#   Sin tocar nada más.
#
# El LLM se usa UNA SOLA VEZ por compilación — authoring time, no runtime.

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

from ...infraestructure.llm.llm import LLMClient
from ..core.models import Fact
from .constraints import Constraint
from .rules import Rule

T = TypeVar("T", bound=BaseModel)

# ─────────────────────────────────────────────────────────────────────────────
# Texto compartido entre prompts
# ─────────────────────────────────────────────────────────────────────────────

_LANGUAGE_RULES = (
    "The description may be written in any language (English, Spanish, etc.).\n"
    "Regardless of the input language, ALL output field values must be in English:\n"
    "  - names and fact_kind/fact_name identifiers must be English snake_case.\n"
    "  - string values in conditions must also be in English.\n"
    "This ensures the engine works consistently regardless of the author's language.\n"
)

_CONDITION_DOCS = (
    "- when: a list of Condition objects, each with:\n"
    "    - fact_kind: the category of the fact (e.g. 'perception', 'decision')\n"
    "    - fact_name: the name of the fact (e.g. 'intent', 'confidence')\n"
    "    - op: one of '==', '!=', '>', '>=', '<', '<=', 'in', 'not_in', 'contains'\n"
    "         use 'contains' when checking if a string fact contains a substring\n"
    "         use 'in' only when checking if a fact value is a member of a collection\n"
    "    - value: the value to compare against (in English if it is a string)\n"
)

# ─────────────────────────────────────────────────────────────────────────────
# System prompts por tipo
# ─────────────────────────────────────────────────────────────────────────────

_RULE_SYSTEM_PROMPT = (
    "You are a rule compiler for a cognitive AI architecture.\n"
    "The user will describe a business rule in natural language.\n"
    + _LANGUAGE_RULES
    + "\nYour job is to translate the description into a structured Rule with:\n\n"
    "- name: a short snake_case identifier for the rule\n"
    + _CONDITION_DOCS
    + "- then_facts: a list of facts to derive when all conditions are met, each with:\n"
    "    - kind: category of the derived fact (English)\n"
    "    - name: name of the derived fact (English)\n"
    "    - value: value to assign (in English if it is a string)\n\n"
    "Use sensible fact_kind and fact_name names based on context.\n"
    "Respond only with the JSON matching the schema provided."
)

_CONSTRAINT_SYSTEM_PROMPT = (
    "You are a constraint compiler for a cognitive AI architecture.\n"
    "The user will describe a business constraint (a guardrail or validation rule) in natural language.\n"
    + _LANGUAGE_RULES
    + "\nYour job is to translate the description into a structured Constraint with:\n\n"
    "- name: a short snake_case identifier for the constraint\n"
    "- message: a clear human-readable explanation of what went wrong when the constraint fires\n"
    "- severity: one of 'low', 'medium', 'high' based on the business impact described\n"
    + _CONDITION_DOCS
    + "\nUse sensible fact_kind and fact_name names based on context.\n"
    "Respond only with the JSON matching the schema provided."
)

# ─────────────────────────────────────────────────────────────────────────────
# Base genérica
# ─────────────────────────────────────────────────────────────────────────────

class LLMSymbolicCompiler(ABC, Generic[T]):
    """
    Base genérica para compiladores simbólicos.

    Cada subclase solo necesita declarar `_system_prompt` y `_output_model`.
    Toda la lógica de construcción del prompt y la llamada al LLM vive aquí.
    """

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    @property
    @abstractmethod
    def _system_prompt(self) -> str: ...

    @property
    @abstractmethod
    def _output_model(self) -> Type[T]: ...

    async def compile(
        self,
        description: str,
        available_facts: Optional[List[Fact]] = None,
    ) -> T:
        """
        Translate a natural language description into a validated Pydantic model.

        Parameters
        ----------
        description : plain-language description of the rule or constraint, in any language.
        available_facts : optional list of facts already in the system.
            When provided, the compiler uses their (kind, name) pairs as the
            canonical vocabulary, ensuring generated conditions match real facts.
        """
        prompt = f"Compile: {description}"

        if available_facts:
            schema_lines = "\n".join(
                f"  - kind={f.kind!r}, name={f.name!r}, example_value={f.value!r}"
                for f in available_facts
            )
            prompt += (
                "\n\nAvailable facts in the system. Use ONLY these (kind, name) pairs "
                "in your conditions, and choose the most specific fact that fits the intent.\n"
                "For string containment checks use op='contains'.\n"
                + schema_lines
            )

        return await self._llm.think(
            prompt=prompt,
            context=self._system_prompt,
            output_model=self._output_model,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Implementaciones concretas
# ─────────────────────────────────────────────────────────────────────────────

class LLMRuleCompiler(LLMSymbolicCompiler[Rule]):
    """Compiles a natural language Rule description into a typed Rule."""

    @property
    def _system_prompt(self) -> str:
        return _RULE_SYSTEM_PROMPT

    @property
    def _output_model(self) -> Type[Rule]:
        return Rule


class LLMConstraintCompiler(LLMSymbolicCompiler[Constraint]):
    """Compiles a natural language Constraint description into a typed Constraint."""

    @property
    def _system_prompt(self) -> str:
        return _CONSTRAINT_SYSTEM_PROMPT

    @property
    def _output_model(self) -> Type[Constraint]:
        return Constraint
