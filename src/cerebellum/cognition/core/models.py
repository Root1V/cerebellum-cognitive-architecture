

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    step:   int = Field(description="Execution order of this step, starting at 1.")
    action: str = Field(description="Name of the tool or cognitive action to invoke, e.g. 'search_market_data' or 'analyze_trends'.")
    goal:   str = Field(description="Specific sub-objective this step must accomplish, expressed as a concrete outcome.")


class Plan(BaseModel):
    steps: list[PlanStep] = Field(description="Ordered list of steps that fully decompose the goal. Each step maps to one tool or action.")


class InputType(str, Enum):
    TEXT = "text"
    EVENT = "event"
    STRUCTURED = "structured"


class Fact(BaseModel):
    kind:       str   = Field(description="Category or type of the fact, e.g. 'market_data', 'user_preference'.")
    name:       str   = Field(description="Unique identifier or label for this fact within its kind.")
    value:      Any   = Field(description="The actual content or data of the fact.")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score for this fact, between 0.0 and 1.0.")
    metadata:   Dict[str, Any] = Field(default_factory=dict, description="Optional extra attributes for this fact.")


class ConstraintViolation(BaseModel):
    name:     str  = Field(description="Identifier of the violated constraint, e.g. 'max_budget_exceeded'.")
    message:  str  = Field(description="Human-readable explanation of why the constraint was violated.")
    severity: str  = Field(default="medium", description="Impact level of the violation: 'low', 'medium', or 'high'.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional extra context about the violation.")


class Decision(BaseModel):
    name:     str  = Field(description="Short identifier for the decision taken, e.g. 'use_llm_planner'.")
    reason:   str  = Field(description="Justification or rationale behind the decision.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional extra context or evidence supporting the decision.")


class ActionResult(BaseModel):
    action:   str  = Field(description="Name of the action that was executed.")
    success:  bool = Field(description="True if the action completed without errors, False otherwise.")
    output:   Any  = Field(default=None, description="Return value or data produced by the action, if any.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional extra details such as duration, retries, or error info.")


class NeuralInterpretation(BaseModel):
    intent:          Optional[str] = Field(default=None, description="High-level intent inferred from the input, e.g. 'schedule_meeting'.")
    entities:        Dict[str, Any] = Field(default_factory=dict, description="Named entities or key-value pairs extracted from the input.")
    summary:         Optional[str] = Field(default=None, description="Brief natural-language summary of the input content.")
    extracted_facts: List[Fact]    = Field(default_factory=list, description="Structured facts derived from the input during interpretation.")
    confidence:      float         = Field(default=0.5, ge=0.0, le=1.0, description="Overall confidence in this interpretation, between 0.0 and 1.0.")


class PerceptionResult(BaseModel):
    input_type:     InputType                      = Field(description="Category of the incoming input: text, event, or structured data.")
    raw:            Any                            = Field(description="Original unprocessed input as received from the environment.")
    normalized:     Dict[str, Any]                 = Field(default_factory=dict, description="Parsed and normalized representation of the raw input.")
    interpretation: Optional[NeuralInterpretation] = Field(default=None, description="Structured semantic interpretation produced by the perception layer.")



class CognitiveState(BaseModel):
    goal:           Optional[str]              = Field(default=None, description="High-level objective the agent is currently pursuing.")
    input_text:     Optional[str]              = Field(default=None, description="Raw input text received at the start of the current cognitive cycle.")

    context:        Dict[str, Any]             = Field(default_factory=dict, description="Shared key-value context passed across cognitive components during a cycle.")

    facts:          List[Fact]                 = Field(default_factory=list, description="Accumulated facts gathered or inferred during the current cycle.")
    decisions:      List[Decision]             = Field(default_factory=list, description="Decisions taken by the agent during the current cycle.")
    constraints:    List[ConstraintViolation]  = Field(default_factory=list, description="Constraint violations detected during planning or execution.")
    plan:           List[PlanStep]             = Field(default_factory=list, description="Ordered sequence of steps produced by the planner for the current goal.")
    action_results: List[ActionResult]         = Field(default_factory=list, description="Results collected from actions executed during the current cycle.")

    working_notes:  List[str]                  = Field(default_factory=list, description="Informal scratchpad notes written by reasoning components.")
    trace:          List[str]                  = Field(default_factory=list, description="Ordered log of significant events and state transitions in the cycle.")

    def add_trace(self, message: str) -> None:
        self.trace.append(message)
