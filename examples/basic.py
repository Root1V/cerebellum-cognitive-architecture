# examples/research_basic.py
#
# Ejemplo mínimo del ciclo cognitivo completo.
# Usa las implementaciones más simples de cada módulo.

import asyncio

from dotenv import load_dotenv

load_dotenv()


from cerebellum.cognition.action import ConsoleAction
from cerebellum.cognition.attention import SimpleAttention
from cerebellum.cognition.core import CognitiveAgent
from cerebellum.cognition.learning import SimpleLearning
from cerebellum.cognition.memory import EpisodicMemory, WorkingMemory
from cerebellum.cognition.perception import TextPerception
from cerebellum.cognition.planners import SimplePlanner
from cerebellum.cognition.reasoning import LoopReasoner
from cerebellum.cognition.runtime import CognitiveSystem
from cerebellum.environment import TextEnvironment
from cerebellum.cognition.controller import SimpleController
from cerebellum.infraestructure.llm.llm_client import LLMClient
from cerebellum.cognition.neural.llm_neural import LLMNeuralEngine
from cerebellum.cognition.symbolic import DeclarativeRuleEngine, LLMRuleCompiler, Rule, Condition
from cerebellum.cognition.core.models import Fact


async def main():

    llm = LLMClient(
        model="Mixtral-7B-Instruct-v0.1.Q4_0.gguf",
        timeout=60.0,
    )

    # ─────────────────────────────────────────────
    # 1. NEURAL LAYER — interpret raw text
    # ─────────────────────────────────────────────
    perception = TextPerception(neural_engine=LLMNeuralEngine(llm))
    perception_result = await perception.perceive(
        "Analyze the AI market in LATAM, focusing on startups and investment trends."
    )

    print("\n── PERCEPTION ──")
    print(perception_result)

    # ─────────────────────────────────────────────
    # 4. DERIVE FACTS from the perception result
    #    Convert NeuralInterpretation → List[Fact]
    #    so the rule engine can reason over them.
    # ─────────────────────────────────────────────
    base_facts: list[Fact] = []

    if perception_result.interpretation:
        interp = perception_result.interpretation
        base_facts = [
            Fact(kind="perception", name="intent",     value=interp.intent,     confidence=interp.confidence),
            Fact(kind="perception", name="confidence", value=interp.confidence, confidence=1.0),
            Fact(kind="perception", name="summary",    value=interp.summary,    confidence=1.0),
        ]
        # Add any extracted facts from the neural interpretation directly
        base_facts.extend(interp.extracted_facts)

    # ─────────────────────────────────────────────
    # 2. SYMBOLIC LAYER — author rules via LLM
    #    (done once at startup / config time)
    # ─────────────────────────────────────────────
    compiler = LLMRuleCompiler(llm_client=llm)

    # Each .compile() call happens ONCE — the LLM translates natural language
    # into a deterministic Rule that the engine runs with no further LLM calls.
    # Rules can be authored in any language — the compiler normalizes output to English.
    # Passing available_facts ensures generated conditions match the real fact vocabulary.
    rule_search_required = await compiler.compile(
        "If intent is 'research' and confidence is above 0.7, "
        "mark that an external search is required.",
        available_facts=base_facts,
    )
    rule_low_confidence = await compiler.compile(
        "If confidence is below 0.9, flag the result as unreliable.",
        available_facts=base_facts,
    )
    rule_mercado_latam = await compiler.compile(                          # Spanish
        "Si la región del mercado es 'LATAM', marcar que se requiere "
        "un análisis regional específico.",
        available_facts=base_facts,
    )

    print("\n── COMPILED RULES ──")
    print(rule_search_required)
    print(rule_low_confidence)
    print(rule_mercado_latam)

    # ─────────────────────────────────────────────
    # 3. BUILD ENGINE with the compiled rules
    # ─────────────────────────────────────────────
    engine = DeclarativeRuleEngine(rules=[rule_search_required, rule_low_confidence, rule_mercado_latam])

    derived_facts = engine.derive(base_facts)

    print("\n── BASE FACTS ──")
    for f in base_facts:
        print(f" • [{f.kind}] {f.name} = {f.value!r}  (confidence={f.confidence})")

    print("\n── DERIVED FACTS (rules fired) ──")
    if derived_facts:
        for f in derived_facts:
            print(f" • [{f.kind}] {f.name} = {f.value!r}")
    else:
        print("  (no rules fired)")


asyncio.run(main())