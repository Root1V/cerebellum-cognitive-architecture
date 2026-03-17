from typing import Any, Dict, Optional, Literal
from pydantic import BaseModel, Field

class MemoryStorePayload(BaseModel):
    """Payload para pedir guardar algo en memoria."""
    scope: Literal["working", "episodic", "semantic"]
    key: str
    value: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)

class MemoryRecallPayload(BaseModel):
    """Payload para pedir recuperar algo por clave."""
    scope: Literal["working", "episodic", "semantic"]
    key: str

class MemoryAvailablePayload(BaseModel):
    """Payload con el resultado de una recuperación de memoria."""
    id: str # ID del mensaje original (correlation)
    data: Optional[Any] = None
    found: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
