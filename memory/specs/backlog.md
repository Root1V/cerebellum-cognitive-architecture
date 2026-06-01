# Cerebellum SDD Backlog

Based on pre-SDD codebase audit (May 31, 2026). Specs to be created and implemented in priority order.

---

## Phase 1 — Stabilize & Fix (Critical)

### [001] Fix Blocking I/O in EmbeddingClient

**Priority:** CRITICAL  
**Complexity:** Trivial (1-line fix)  
**Effort:** 1 hour

**Problem:**
`infraestructure/llm/embedd_client.py:45` calls `self._model.encode()` synchronously inside an `async def`, blocking the entire event loop during attention and episodic memory operations.

**Impact:** Stalls cognitive loop during `SimpleAttentionModule` and `EpisodicMemory` operations.

**Solution:**
Use `asyncio.to_thread()` (Python 3.13) to offload CPU-bound encoding to thread pool.

**Files to change:**
- `src/cerebellum/infraestructure/llm/embedd_client.py`

**Acceptance Criteria:**
- [ ] `encode()` no longer blocks event loop
- [ ] Tests pass for attention focus updates
- [ ] Tests pass for episodic memory store/search

---

### [002] Remove Dead Code & Fix Production Issues

**Priority:** HIGH  
**Complexity:** Low  
**Effort:** 2 hours

**Problem:**
- 5 stub/orphaned files clutter the codebase
- 1 `print()` statement in `tracer.py` violates logging standards
- Test coverage weak (~10%)

**Solution:**
1. Delete orphaned files
2. Replace `print()` with `logger.debug()`
3. Stabilize existing test suite and add coverage targets

**Files to delete:**
- `src/cerebellum/cognition/runtime/event_loop.py` (unused)
- `src/cerebellum/cognition/runtime/rules.py` (orphaned)
- `src/cerebellum/cognition/perception/multimodal_perception.py` (stub)
- `src/cerebellum/cognition/planners/task_graph_planner.py` (stub)
- `src/cerebellum/tools/code_executor.py` (stub)

**Files to modify:**
- `src/cerebellum/infraestructure/observability/tracer.py` (remove print)

**Acceptance Criteria:**
- [ ] All 5 dead files deleted
- [ ] No `print()` statements in production code
- [ ] All tests pass with `uv run pytest tests/ -v`
- [ ] Coverage report generated

---

## Phase 2 — Strengthen Architecture (High Priority)

### [003] Wire Observability Into Cognitive Loop

**Priority:** HIGH  
**Complexity:** Medium  
**Effort:** 6 hours

**Problem:**
Observability stubs exist but are not integrated into `CognitiveRuntime` and cognitive modules. Cannot trace agent execution in production.

**Solution:**
1. Integrate `tracer` into `CognitiveRuntime.run_until_idle()` and module message handlers
2. Define span naming convention: `<domain>.<action>` (e.g. `perception.process`, `memory.recall`)
3. Emit structured log events at key cognitive transitions
4. Add metrics counter for messages processed per module

**Files to modify:**
- `src/cerebellum/cognition/runtime/cognitive_runtime.py`
- `src/cerebellum/cognition/*/` (all modules)
- `src/cerebellum/infraestructure/observability/tracer.py`
- `src/cerebellum/infraestructure/observability/metrics.py`

**Acceptance Criteria:**
- [ ] Every module emits `on_start`, `on_message`, `on_stop` spans
- [ ] CognitiveRuntime emits `runtime.idle_cycle` span
- [ ] All spans include correlation_id
- [ ] Integration tests verify span chain

---

### [004] Tool Registry with Pydantic Validation

**Priority:** HIGH  
**Complexity:** Medium  
**Effort:** 8 hours

**Problem:**
`MotorCortexModule` has a bare `dict` of tools with no schema validation. Tools can receive any input from the reasoning layer — a vector for RCE/injection attacks.

**Solution:**
1. Define `Tool` ABC with input/output schema (pydantic BaseModel)
2. Create `ToolRegistry` that validates all tool inputs before execution
3. Define built-in tools: `web_search`, `database_query`, `code_analysis` with proper schemas
4. Add tool result caching to prevent redundant calls

**Files to create:**
- `src/cerebellum/tools/registry.py` (new)
- `src/cerebellum/tools/built_in/` (new package)
  - `web_search.py`
  - `database_query.py`
  - `code_analysis.py`

**Files to modify:**
- `src/cerebellum/tools/tool.py` (formalize ABC)
- `src/cerebellum/cognition/action/motor_cortex.py`

**Acceptance Criteria:**
- [ ] All tool inputs validated with pydantic before execution
- [ ] Tool results cached with TTL
- [ ] Invalid inputs rejected with clear error
- [ ] Tests cover injection attempts

---

### [005] Timeout, Cancellation & Error Recovery

**Priority:** HIGH  
**Complexity:** Medium  
**Effort:** 6 hours

**Problem:**
`CognitiveRuntime.run_until_idle()` can hang if a module handler blocks or loops infinitely. No graceful cancellation. No error recovery.

**Solution:**
1. Add `timeout` parameter to `run_until_idle(timeout_seconds=30)`
2. Wrap each handler call in `asyncio.timeout()` per-module with individual timeouts
3. Implement dead letter queue (DLQ) for failed messages
4. Add exponential backoff retry logic for transient failures

**Files to modify:**
- `src/cerebellum/cognition/runtime/cognitive_runtime.py`
- `src/cerebellum/cognition/runtime/event_bus.py` (add DLQ)
- `src/cerebellum/cognition/runtime/types.py` (add retry metadata)

**Acceptance Criteria:**
- [ ] Runtime respects timeout and cancels pending handlers
- [ ] Failed messages move to DLQ
- [ ] Retries use exponential backoff
- [ ] Integration tests verify cancellation under load

---

## Phase 3 — Scale to Multi-Agent (Medium Priority)

### [006] Multi-Runtime & Agent-to-Agent Protocol

**Priority:** MEDIUM  
**Complexity:** High  
**Effort:** 16 hours

**Problem:**
Current architecture supports only a single `CognitiveRuntime`. No way to spawn multiple independent agents or create a swarm. Communication is broadcast-only (no routing).

**Solution:**
1. Introduce `AgentPool` manager to spawn and manage multiple runtimes
2. Define agent identity protocol: `agent.<name>` as sender/receiver
3. Implement topic-level agent routing: `perception.process[agent-id]` format
4. Add `AgentRegistry` for service discovery
5. Implement inter-agent message forwarding via EventBus

**Files to create:**
- `src/cerebellum/cognition/runtime/agent_pool.py` (new)
- `src/cerebellum/cognition/runtime/agent_registry.py` (new)

**Files to modify:**
- `src/cerebellum/cognition/runtime/types.py` (Message with agent routing)
- `src/cerebellum/cognition/runtime/event_bus.py` (routing logic)
- `src/cerebellum/cognition/core/agent.py` (multi-agent interface)

**Acceptance Criteria:**
- [ ] Multiple CognitiveRuntimes coexist in single AgentPool
- [ ] Messages route correctly between agents
- [ ] Agent registry tracks alive/dead agents
- [ ] Integration tests verify agent-to-agent messaging

---

### [007] Agent-to-Agent Routing & Delegation

**Priority:** MEDIUM  
**Complexity:** High  
**Effort:** 12 hours

**Problem:**
No way for one agent to delegate tasks to another. No dynamic routing. No subscription-based agent targeting.

**Solution:**
1. Define `DelegationPayload` and `DelegationResultPayload` protocols
2. Implement `DelegationModule` that routes work to specialized agents based on capability tags
3. Add agent capability advertisement (e.g. `capabilities: ["vision", "nlp", "planning"]`)
4. Implement load balancing across capable agents
5. Add result aggregation for fan-out / fan-in patterns

**Files to create:**
- `src/cerebellum/cognition/runtime/delegation.py` (new)
- `src/cerebellum/cognition/runtime/load_balancer.py` (new)

**Files to modify:**
- `src/cerebellum/cognition/runtime/protocols.py` (delegation payloads)
- `src/cerebellum/cognition/runtime/agent_registry.py`

**Acceptance Criteria:**
- [ ] Agent can delegate task to another agent by capability
- [ ] Results aggregated and returned
- [ ] Load balancer distributes work fairly
- [ ] Tests verify fan-out/fan-in patterns

---

## Phase 4 — Advanced Features (Lower Priority)

### [008] Metacognition Module (Deferred)

Placeholder for future self-monitoring and meta-level reasoning.

### [009] Procedural Memory (Deferred)

Placeholder for skill/procedure recording and replay.

### [010] HTTP API Gateway (Deferred)

Expose CognitiveRuntime + AgentPool via FastAPI with RFC 9457 problem details.

---

## Summary

| Phase | Specs | Effort | Start |
|-------|-------|--------|-------|
| 1. Stabilize | 001–002 | ~3h | Week 1 |
| 2. Strengthen | 003–005 | ~20h | Week 1–2 |
| 3. Scale | 006–007 | ~28h | Week 2–3 |
| 4. Advanced | 008–010 | TBD | Q3 |
| **TOTAL** | **7 active** | **~51h** | **3 weeks** |

---

## Notes for spec-writer-agent

- Each spec must be ≤15 ACs
- All specs inherit from the `.github/copilot-instructions.md` three laws
- All specs reference `.github/instructions/testing.instructions.md` for test patterns
- Every new module must inherit `CognitiveModule` and register in `CognitiveRuntime`
- All payloads must use pydantic models in `protocols.py`
- No spec may introduce direct module-to-module coupling
