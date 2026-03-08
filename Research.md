Cerebellum 

Es una propuesta de arquitectura cognitiva moderna para agentes. básicamente el blueprint que muchos laboratorios de investigación están explorando para construir sistemas más cercanos a una inteligencia general. La idea central un "sistema cognitivo", este se construye con múltiples subsistemas cognitivos.

1.-Arquitectura General
                 USER
                   │
                   ▼
             Perception Layer
                   │
                   ▼
            Cognitive Controller
      ┌───────────┼───────────┐
      │           │           │
   Memory      Reasoning     Planning
      │           │           │
      └───────────┼───────────┘
                  │
               Tool Layer
                  │
             Environment
                  │
             Observability


Ideas clave: El LLM vive dentro del Reasoning Engine, no es todo el sistema.

2. Componentes principales de una Cognitive Agent Architecture

2.1 Perception Layer: 
Es la capa que interpreta el mundo. Entrada posible:
-texto
-audio
-imágenes
-documentos
-APIs
-eventos del sistema

Ejemplo: User question, PDF document, Database records, Audio input

La percepción transforma todo eso en representaciones estructuradas:

Ejmplo: Intent, Entities, Context, Goal

2.2 Cognitive Controller (el “cerebro ejecutivo”):
Este componente decide qué hacer a continuación. Funciona parecido al cortex prefrontal en humanos.

Responsabilidades:
-goal tracking
-task switching
-agent coordination
-reasoning orchestration

Ejemplo:
User goal detected
↓
Create plan
↓
Assign subtask to reasoning engine
↓
Call tools
↓
Store memory

Este controlador puede ser:
-un LLM
-un planner
-un state machine
-un policy model

2.3 Memory System: 
Una arquitectura cognitiva real necesita varios tipos de memoria.

2.3.1 Working Memory: Memoria temporal para el pensamiento actual.
Ejemplo:
-current task
-recent reasoning steps
-intermediate results

2.3.2 Episodic Memory: Recuerdos de experiencias pasadas.
Ejemplo:
-conversation history
-past actions
-previous tasks

2.3.3 Semantic Memory: Conocimiento del mundo.
Ejemplo:
-facts
-documents
-knowledge base

2.3.4 Procedural Memory: Cómo hacer cosas.
Ejemplo:
-tool usage
-workflows
-skills

Muchos sistemas usan:
-vector DB
-graph DB
-document stores

para implementarlas.

2.4 Reasoning Engine:
Aquí es donde vive el LLM(Large Language Model) o LRM (Larg Reasoning Model)
Este módulo realiza:
-analysis
-deduction
-hypothesis generation
-problem solving

Puede usar técnicas como:
-chain-of-thought
-tree-of-thought
-recursive reasoning
-HRM (Hierarchical Reasoning Model)

Ejemplo de flujo:
Problem
↓
Generate reasoning path
↓
Evaluate
↓
Select best solution


2.5 Planner:
Divide objetivos complejos.

Ejemplo:
2.5.1 Goal: Write a market analysis
2.5.2 Plan:
-1 Collect data
-2 Analyze trends
-3 Create charts
-4 Write report

El planner puede usar:
-LLM
-planning algorithms
-task graphs


2.6 Tool / Action Layer:
Permite actuar en el mundo real.
Ejemplos:
-API calls
-database queries
-web browsing
-code execution
-robot control

Aquí aparecen los agentes especializados.


2.7 Learning Loop:
Un sistema cognitivo real aprende de la experiencia.
Ciclo:
Action
↓
Observation
↓
Evaluation
↓
Memory update

Esto permite:
-mejorar prompts
-aprender workflows
-optimizar decisiones


3. Observability (muy importante en sistemas reales)
Este componente monitorea:
-reasoning steps
-tool usage
-latency
-errors
-decision paths

Herramientas como Langfuse hacen esto parcialmente. Pero una arquitectura cognitiva lo integra desde el inicio.


4. Insight importante:
La mayoría de frameworks actuales solo cubren una pequeña parte de esta arquitectura.
Ejemplo:
Framework	- Lo que cubre
LangGraph	-> agent orchestration
AutoGen	    -> multi-agent coordination
Semantic Kernel ->	tool orchestration

Ninguno implementa una arquitectura cognitiva completa.


5. Lo que muchos investigadores creen que vendrá
La siguiente generación de sistemas de IA probablemente será:

Foundation Models
+
Reasoning Models
+
Cognitive Architectures
+
Cognitive Agents (Autonomous)

---



Environment
     │
     ▼
Event Bus
     │
     ▼
Perception
     │
     ▼
Memory Streams
     │
     ▼
Cognitive Controller
     │
     ▼
Reasoning Loop
     │
     ▼
Tools / Actions
     │
     ▼
New Events


Las 7 interfaces cognitivas fundamentales
1. Perception
2. Attention
3. Memory
4. Reasoning
5. Planning
6. Action
7. Learning

Environment
     │
     ▼
Perception
     │
     ▼
Attention
     │
     ▼
Memory
     │
     ▼
Reasoning
     │
     ▼
Planning
     │
     ▼
Action
     │
     ▼
Learning

----
CognitiveController (Executive)
    ✅ interpret(perception) → "¿cuál es el goal que el agente debe perseguir?"
    ✅ is_goal_satisfied(result, goal) → "¿ya terminamos?"
    ✅ next_goal(history) → "¿hay un subgoal derivado?"

Planner
    ✅ create_plan(goal) → "¿cómo lo logramos? (pasos concretos)"

CognitiveSystem
    ✅ Orquesta el ciclo
    ✅ Decide cuántos ciclos correr y cuándo detenerse

