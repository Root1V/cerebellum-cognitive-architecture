# Changelog

## [0.2.0](https://github.com/Root1V/cerebellum-cognitive-architecture/compare/v0.1.3...v0.2.0) (2026-03-17)


### Features

* implement message-driven choreography and working memory refactor ([0938449](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/09384499b3acb9ba5b2539a050951d5f06d5ad02))
* implement message-driven cognitive runtime and refactor working memory ([43dd070](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/43dd0704057ac5cb73f7b49d963a9e0d6a498fe7))
* refactor episodic memory as a message-driven cognitive module ([1289331](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/12893317e0bbec3722c7b67ef98d9ab8d45da26e))
* refactor episodic memory as a message-driven cognitive module ([0545627](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/05456275aab7799bfeb66ec7a906e759553b5c9d))
* refactor semantic memory as a message-driven cognitive module ([c48c7b1](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/c48c7b177afac994b291952cff37bce04cb73924))
* refactor semantic memory as a message-driven cognitive module ([956aab4](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/956aab40ddb655d8fc1da755c0a299d6f23016e6))


### Documentation

* document branching strategy and development workflow in AGENTS.md and copilot-instructions ([d580bc9](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/d580bc915f066acbfce1cee36561b50079e4a558))
* establish Event-Driven Choreography as core architectural principle ([5e8feaa](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/5e8feaa9e807a73ca61e8ae1fd37db4142363caf))

## [0.1.3](https://github.com/Root1V/cerebellum-cognitive-architecture/compare/v0.1.2...v0.1.3) (2026-03-16)


### Bug Fixes

* **ci:** resolve remaining CI issues (new PR) ([774717a](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/774717a571f55406faf498a0fbd81e0e94b4d9f1))

## [0.1.2](https://github.com/Root1V/cerebellum-cognitive-architecture/compare/v0.1.1...v0.1.2) (2026-03-16)


### Bug Fixes

* **ci:** resolve remaining CI issues ([be59f01](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/be59f019750395a2d9fb22c66df4fa5767cf288d))

## [0.1.1](https://github.com/Root1V/cerebellum-cognitive-architecture/compare/v0.1.0...v0.1.1) (2026-03-16)


### Bug Fixes

* correcciones en github agents y prompts ([11534c9](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/11534c904c41d4f853a99cd4d975efdf41f29001))
* install bandit[sarif] extra and update codeql-action to v4 ([e0a3835](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/e0a3835b23b3360ff8c8d05e980c94c19327ae5b))
* reformat github agents markdown to follow best practices ([4354add](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/4354adde9c2a83fe9aa04e4d184cbb26d8948673))
* remove unused imports in db_episodic.py ([5a27e1a](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/5a27e1a37d36248ddd4a88bc602509a07ef555d7))
* resolve all mypy type-checking errors in src directory ([fe3dd57](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/fe3dd5750c7ee02217354c56ad696a7c178245b1))


### Documentation

* deeply improve AGENTS.md globally for human and AI agents ([675cae0](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/675cae081b48bab50107c582f186281296b3ed2a))
* deeply improve architecture and coding instructions for copilot ([1615258](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/1615258e6b53bbeb1069b576da689b589cc200f1))
* enhance github copilot instructions, prompts and skills ([73bebfc](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/73bebfcdff57306818e85673f23063f5b15881c7))
* enrich copilot-instructions.md with cerebellum-specific context and rules ([e20b36d](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/e20b36dbc320d05388389cf27f97628843c6e2b6))

## 0.1.0 (2026-03-15)


### Features

* actualiza episodic_memory.py y agrega archivos nuevos ([6ee593d](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/6ee593d7dabe22b18b38940f6abd6ecd296faf5c))
* actualiza episodic_memory.py y agrega archivos nuevos ([e730b15](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/e730b1538a22a891a117c1e1f6fdefa08df557dc))
* add LoopReasoner — replace sequential reasoning with a think→act→evaluate loop ([043d123](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/043d12352e621efe824c2a1aa2787b89f6fe8c6d))
* Integrate axonium SDK via LlamaAdapter for local LLM support ([#6](https://github.com/Root1V/cerebellum-cognitive-architecture/issues/6)) ([a2fca36](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/a2fca363b5e30199626bc88791b63a1f21aaf674))
* LLMClient ABC + think() contract + typed Plan/PlanStep structured output ([#10](https://github.com/Root1V/cerebellum-cognitive-architecture/issues/10)) ([ad69f93](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/ad69f93f17e7bdb4399cb01b0952ed1b34f127ad))
* LoopReasoner + architecture coherence pass (P0/P1/P2/P3) ([6b7c4c5](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/6b7c4c5c67bdbb459f65c7a327420c42bd0b50d4))
* LoopReasoner + architecture coherence pass (P0/P1/P2/P3) ([6b7c4c5](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/6b7c4c5c67bdbb459f65c7a327420c42bd0b50d4))
* mejoras arquitectura cognitiva y tests robustos ([59a4e8c](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/59a4e8cf80c69708247415b40c328510370d74d3))
* neural + symbolic cognitive layers with bilingual rule compiler ([29f7eae](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/29f7eaea2472f813aff4c7c6237ff6335ab1a932))
* neural + symbolic cognitive layers with bilingual rule compiler ([c527ae6](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/c527ae691e87f83ccd3a4d327d86b08c35e497ae))


### Bug Fixes

* annotate CognitiveSystem instance attrs and wire context into planner ([ce86b04](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/ce86b04a0e97cfb0524ccded1be14b0fe7997d42))
* architecture cleanup - type annotations, hints, and design consistency ([5588f01](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/5588f01dc699ac058d986e4741d1368cc0f376c9))
* architecture cleanup — reasoners, broken example, docstrings ([d940293](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/d94029368b4c5b971d2dda364522eb18e1d1e3a9))
* code quality — type hints on all ABCs, implementations, and system entrypoints ([37d5d46](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/37d5d4657b3f549b9bb7f04ffbab3e5bbba860d9))
* elimina duplicado de name en release.yml ([34ec4fa](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/34ec4faaae8444a0c2ada465392f462a1367ab1a))
* **group-1:** annotate self attributes in WorkingMemory, EpisodicMemory, SemanticMemory, MemoryStream, DatabaseTool, Metrics ([e838b19](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/e838b198b0644c18cd4c7d6975ffa9c9ae6d12d0))
* **group-2:** correct wrong type hints — ConsoleAction tools dict, SemanticMemory Any, Attention perception param ([8c7739d](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/8c7739d6d8c0fd47ba3582e65f404519dfde2530))
* **group-3:** add param and return type annotations to WorkingMemory, TextPerception, WebSearchTool, Tracer, Metrics, SimplePlanner ([d2a05c7](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/d2a05c7966bff67752bd0c037cbd195843cc16bf))
* **group-A:** add param and return type hints to all 7 core ABCs; fix Reasoner memory param to dict[str,Memory] ([69468d4](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/69468d47ea2fc5b685c8718937f2c95d775abadd))
* **group-B:** fix memory:dict[str,Memory] in all reasoners, correct controller.interpret param(dict), add param types to EpisodicMemory/SemanticMemory/MemoryStream, fix MemoryStream.add KeyError ([3738081](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/3738081c43ef48b06fbbe92e89c3f17be94b6c04))
* **group-C:** type CognitiveSystem.run(str)-&gt;Any, add recursion depth guard(_MAX_GOAL_DEPTH=5), type CognitiveAgent.run(str)-&gt;Any ([63ae1d8](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/63ae1d8b4d1130329d9ad2f14b7d591807853641))
* ids únicos en EventMemory, mejoras en impresión y ejemplo de memoria episódica ([d85d810](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/d85d81009f95fc302e91a5a648c20663a5055a22))
* P0/P1/P2/P3 architecture coherence pass ([a739553](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/a73955354ee9b29ca01f96c9c67b1b125dc1554e))
* semantic and flow improvements — wire action/env/metrics, fix duplication and completion logic ([#5](https://github.com/Root1V/cerebellum-cognitive-architecture/issues/5)) ([fc9ca5c](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/fc9ca5ca46bed864c05c3a473433eaabb0bdb66a))
* semantic review ([#7](https://github.com/Root1V/cerebellum-cognitive-architecture/issues/7)) ([d33ab56](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/d33ab568d3dc55077e22468c7fb35b7c064c3f61))


### Documentation

* add Level 0 cognitive architecture diagram to README ([9f41e31](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/9f41e31ea8715f9b44b691f77527482ef70453d6))
* fix README corrections; update pyproject and lock file ([#9](https://github.com/Root1V/cerebellum-cognitive-architecture/issues/9)) ([5092749](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/5092749876046c761a1cd4b2cc96c054b5dac38a))
* rewrite README with C4 context and container diagrams ([5fabe27](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/5fabe2768976b8fc419f125234d87d6b9ced0cf3))
* rewrite README with C4 context and container diagrams ([7e0a215](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/7e0a2158034548599aff3484fc2770f7ade9aa03))
* wrap Level 0 diagram in code block for proper rendering ([17f2f5f](https://github.com/Root1V/cerebellum-cognitive-architecture/commit/17f2f5f236db50b8924db02f0422d172c45293e1))
