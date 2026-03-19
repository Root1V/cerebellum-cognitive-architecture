from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field
from ..core.models import PerceptionResult, Plan

class MemoryStorePayload(BaseModel):
    """Payload para pedir guardar algo en memoria."""
    scope: Literal["working", "episodic", "semantic"]
    key: str
    value: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemoryRecallPayload(BaseModel):
    """Payload para pedir recuperar algo por clave exacto."""
    scope: Literal["working", "episodic", "semantic"]
    key: str

class MemorySearchPayload(BaseModel):
    """Payload para búsqueda semántica/similitud (habitual en Episodic)."""
    query: str
    limit: int = 5
    metadata_filter: Dict[str, Any] = Field(default_factory=dict)

class MemoryAvailablePayload(BaseModel):
    """Payload con el resultado de una recuperación de memoria."""
    id: str # ID del mensaje original (correlation)
    data: Optional[Any] = None
    found: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

# --- Perception Protocols ---

class PerceptionProcessPayload(BaseModel):
    """Payload para solicitar el procesamiento de una entrada cruda."""
    input_type: str = "text"
    raw_data: Any

class PerceptionOutputPayload(BaseModel):
    """Payload emitido tras procesar una percepción."""
    result: PerceptionResult

# --- Attention Protocols ---

class AttentionOutputPayload(BaseModel):
    """Payload emitido tras filtrar y enfocar la atención."""
    focused_result: PerceptionResult
    relevance_score: float = 1.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

# --- Reasoning Protocols ---

class ReasoningOutputPayload(BaseModel):
    """Payload emitido cuando se ha generado un plan de acción."""
    plan: Plan
    goal: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AttentionSetFocusPayload(BaseModel):
    """Payload para actualizar el foco de atención dinámicamente."""
    query: str
