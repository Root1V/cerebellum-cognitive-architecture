# examples/research_basic.py
#
# Ejemplo mínimo del ciclo cognitivo completo.
# Usa las implementaciones más simples de cada módulo.

import asyncio
from typing import List

from dotenv import load_dotenv
load_dotenv()

from cerebellum.cognition.perception import TextPerception
from cerebellum.infraestructure.llm.llm_client import LLMClient
from cerebellum.cognition.neural.llm_neural import LLMNeuralEngine
from cerebellum.cognition.symbolic import (
    DeclarativeRuleEngine,
    LLMRuleCompiler,
    Rule,
    DeclarativeConstraintEngine,
    LLMConstraintCompiler,
    Constraint,
)
from cerebellum.cognition.core.models import Fact



async def perceive_and_extract_facts(llm: LLMClient, text: str) -> List[Fact]:
    """Procesa el texto y extrae hechos base usando el motor neural."""
    perception = TextPerception(neural_engine=LLMNeuralEngine(llm))
    result = await perception.perceive(text)
    print("\n── PERCEPCIÓN ──")
    print(result)
    facts: List[Fact] = []
    if result.interpretation:
        interp = result.interpretation
        # Forzar confianza baja para demo de constraints
        facts = [
            Fact(kind="perception", name="intent", value=interp.intent, confidence=0.4),
            Fact(kind="perception", name="confidence", value=0.4, confidence=1.0),
            Fact(kind="perception", name="summary", value=interp.summary, confidence=1.0),
        ]
        facts.extend(interp.extracted_facts)
    return facts

async def compile_rules(llm: LLMClient, facts: List[Fact]) -> List[Rule]:
    """Compila reglas de negocio usando el LLM."""
    compiler = LLMRuleCompiler(llm_client=llm)
    rules = []
    try:
        rules.append(await compiler.compile(
            "If intent is 'research' and confidence is above 0.7, mark that an external search is required.",
            available_facts=facts,
        ))
        rules.append(await compiler.compile(
            "If confidence is below 0.9, flag the result as unreliable.",
            available_facts=facts,
        ))
        rules.append(await compiler.compile(
            "Si la región del mercado es 'LATAM', marcar que se requiere un análisis regional específico.",
            available_facts=facts,
        ))
    except Exception as e:
            print(f"Error compilando reglas: {e}")
    return rules

async def compile_constraints(llm: LLMClient, facts: List[Fact]) -> List[Constraint]:
    """Compila constraints de negocio usando el LLM."""
    compiler = LLMConstraintCompiler(llm_client=llm)
    constraints = []
    try:
        constraints.append(await compiler.compile(
            "If confidence is below 0.5, report as unreliable result with high severity.",
            available_facts=facts,
        ))
        constraints.append(await compiler.compile(
            "Si se detectó la región LATAM pero no se derivó ningún análisis regional, reportar que falta análisis regional con severidad media.",
            available_facts=facts,
        ))
    except Exception as e:
            print(f"Error compilando constraints: {e}")
    return constraints

async def main():
    """Ejemplo mejorado del ciclo cognitivo completo."""
    llm = LLMClient(
        model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf",
        timeout=60.0,
    )
    texto = "Analyze the AI market in LATAM, focusing on startups and investment trends."
    base_facts = await perceive_and_extract_facts(llm, texto)
    rules = await compile_rules(llm, base_facts)
    
    print("\n── REGLAS COMPILADAS ──")
    for r in rules:
        print(r)
    engine = DeclarativeRuleEngine(rules=rules)
    derived_facts = engine.derive(base_facts)
    print("\n── FACTS BASE ──")
    for f in base_facts:
        print(f" • [{f.kind}] {f.name} = {f.value!r}  (confidence={f.confidence})")
    print("\n── FACTS DERIVADOS (rules fired) ──")
    if derived_facts:
        for f in derived_facts:
            print(f" • [{f.kind}] {f.name} = {f.value!r}")
    else:
        print("  (no rules fired)")
    all_facts = base_facts + derived_facts
    constraints = await compile_constraints(llm, all_facts)
    print("\n── CONSTRAINTS COMPILADOS ──")
    for c in constraints:
        print(c)
    constraint_engine = DeclarativeConstraintEngine(constraints=constraints)
    violations = constraint_engine.validate(all_facts)
    print("\n── VIOLACIONES DE CONSTRAINTS ──")
    if violations:
        for v in violations:
            print(f" ! [{v.severity.upper()}] {v.name}: {v.message}")
    else:
        print("  (no violations)")

if __name__ == "__main__":
    asyncio.run(main())
    


# ── PERCEPCIÓN ──
# input_type=<InputType.TEXT: 'text'> raw='Analyze the AI market in LATAM, focusing on startups and investment trends.' normalized={'text': 'Analyze the AI market in LATAM, focusing on startups and investment trends.', 'length': 75, 'num_words': 12} interpretation=NeuralInterpretation(intent='query', entities={'named': ['AI market', 'LATAM', 'startups', 'investment trends'], 'numbers': []}, summary='The user wants an analysis of the AI market in LATAM with a focus on startups and investment trends.', extracted_facts=[Fact(kind='market_data', name='AI market', value='LATAM', confidence=0.9, metadata={}), Fact(kind='focus', name='startups', value='startups', confidence=1.0, metadata={}), Fact(kind='focus', name='investment trends', value='investment trends', confidence=1.0, metadata={})], confidence=0.85)

# ── REGLAS COMPILADAS ──
# name='high_confidence_research' when=[Condition(fact_kind='perception', fact_name='intent', op='==', value='research'), Condition(fact_kind='perception', fact_name='confidence', op='>', value='0.7')] then_facts=[{'kind': 'decision', 'name': 'external_search_required', 'value': 'true'}]
# name='low_confidence_flag' when=[Condition(fact_kind='perception', fact_name='confidence', op='<', value=0.9)] then_facts=[{'kind': 'perception', 'name': 'reliability_flag', 'value': 'unreliable'}]
# name='require Regional_Analysis' when=[Condition(fact_kind='market_data', fact_name='AI market', op='contains', value='LATAM')] then_facts=[{'kind': 'decision', 'name': 'require_analysis', 'value': 'true'}]

# ── FACTS BASE ──
#  • [perception] intent = 'query'  (confidence=0.4)
#  • [perception] confidence = 0.4  (confidence=1.0)
#  • [perception] summary = 'The user wants an analysis of the AI market in LATAM with a focus on startups and investment trends.'  (confidence=1.0)
#  • [market_data] AI market = 'LATAM'  (confidence=0.9)
#  • [focus] startups = 'startups'  (confidence=1.0)
#  • [focus] investment trends = 'investment trends'  (confidence=1.0)

# ── FACTS DERIVADOS (rules fired) ──
#  • [perception] reliability_flag = 'unreliable'
#  • [decision] require_analysis = 'true'

# ── CONSTRAINTS COMPILADOS ──
# name='confidence_below_threshold' message='The result has a confidence below the threshold and is considered unreliable.' severity='high' when=[Condition(fact_kind='perception', fact_name='confidence', op='<', value='0.5')]
# name='missing_regional_analysis' message='Falta análisis regional derivado para la región LATAM' severity='medium' when=[Condition(fact_kind='perception', fact_name='summary', op='contains', value='LATAM'), Condition(fact_kind='decision', fact_name='require_analysis', op='==', value='true'), Condition(fact_kind='perception', fact_name='summary', op='not_in', value='analysis regional')]

# ── VIOLACIONES DE CONSTRAINTS ──
#  ! [HIGH] confidence_below_threshold: The result has a confidence below the threshold and is considered unreliable.
#  ! [MEDIUM] missing_regional_analysis: Falta análisis regional derivado para la región LATAM