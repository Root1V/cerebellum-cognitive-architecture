# symbolic/rule_compiler.py
#
# LLMRuleCompiler: compila lenguaje natural → Rule tipada (Pydantic).
#
# El LLM se usa UNA SOLA VEZ para traducir la intención del usuario.
# El resultado es una Rule determinista que el DeclarativeRuleEngine
# ejecuta sin intervención del LLM en adelante.
#
# Flujo recomendado:
#   rule = await compiler.compile("Si la intención es pregunta y confianza > 0.6, marcar búsqueda requerida")
#   print(rule)          # el usuario revisa
#   engine.rules.append(rule)

from typing import List, Optional

from ...infraestructure.llm.llm import LLMClient
from ..core.models import Fact
from .rules import Rule

_SYSTEM_PROMPT = (
    "You are a rule compiler for a cognitive AI architecture.\n"
    "The user will describe a business rule in natural language.\n"
    "The description may be written in any language (English, Spanish, etc.).\n"
    "Regardless of the input language, ALL output field values must be in English:\n"
    "  - rule names, fact_kind, fact_name, derived fact kind/name must be English snake_case.\n"
    "  - string values in conditions and then_facts must also be in English.\n"
    "This ensures the rule engine works consistently regardless of the author's language.\n"
    "\n"
    "Your job is to translate the description into a structured Rule with:\n"
    "\n"
    "- name: a short snake_case identifier for the rule\n"
    "- when: a list of Condition objects, each with:\n"
    "    - fact_kind: the category of the fact (e.g. 'perception', 'decision')\n"
    "    - fact_name: the name of the fact (e.g. 'intent', 'confidence')\n"
    "    - op: one of '==', '!=', '>', '>=', '<', '<=', 'in', 'not_in', 'contains'\n"
    "         use 'contains' when checking if a string fact contains a substring\n"
    "         use 'in' only when checking if a fact value is a member of a collection\n"
    "    - value: the value to compare against (in English if it is a string)\n"
    "- then_facts: a list of facts to derive when all conditions are met, each with:\n"
    "    - kind: category of the derived fact (English)\n"
    "    - name: name of the derived fact (English)\n"
    "    - value: value to assign (in English if it is a string)\n"
    "\n"
    "Use sensible fact_kind and fact_name names based on context.\n"
    "Respond only with the JSON matching the schema provided."
)


class LLMRuleCompiler:
    """
    Compiles a natural language rule description into a typed Rule using an LLM.

    The LLM is only invoked once per rule — compilation is a one-time authoring
    step, not part of the cognitive execution loop.

    Example:
        compiler = LLMRuleCompiler(llm_client=llm)
        rule = await compiler.compile(
            "If intent is a query and confidence is above 0.6, mark that a search is required"
        )
        print(rule)   # review before adding to engine
        engine.rules.append(rule)
    """

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    async def compile(
        self,
        description: str,
        available_facts: Optional[List[Fact]] = None,
    ) -> Rule:
        """
        Translate a natural language rule description into a validated Rule.

        Parameters
        ----------
        description : plain-language description of the rule.
        available_facts : optional list of facts already in the system.
            When provided, the compiler uses their (kind, name) pairs as the
            canonical vocabulary, ensuring generated conditions match real facts.

        Returns
        -------
        Rule — validated Pydantic model ready to add to a DeclarativeRuleEngine.
        """
        prompt = f"Compile this rule: {description}"

        if available_facts:
            schema_lines = "\n".join(
                f"  - kind={f.kind!r}, name={f.name!r}, example_value={f.value!r}"
                for f in available_facts
            )
            prompt += (
                f"\n\nAvailable facts in the system. Use ONLY these (kind, name) pairs "
                f"in your conditions, and choose the most specific fact that fits the rule intent.\n"
                f"For string containment checks use op='contains'.\n"
                f"{schema_lines}"
            )

        return await self._llm.think(
            prompt=prompt,
            context=_SYSTEM_PROMPT,
            output_model=Rule,
        )
