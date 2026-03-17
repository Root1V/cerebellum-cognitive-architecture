from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

class Message(BaseModel):
    """
    Representa la unidad básica de comunicación entre lóbulos cognitivos.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(description="Identificador único del mensaje")
    sender: str = Field(description="Nombre del lóbulo o agente emisor")
    receiver: str = Field(description="Nombre del lóbulo o agente receptor (o 'broadcast')")
    topic: str = Field(description="Tipo o categoría del mensaje (ej: 'perception.text', 'memory.store')")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Datos del mensaje")
    timestamp: datetime = Field(default_factory=datetime.now)
    correlation_id: Optional[str] = Field(None, description="ID para seguir el rastro de una cadena de pensamientos/mensajes")

class CognitiveContext(BaseModel):
    """
    Contexto de ejecución para un ciclo cognitivo específico.
    """
    run_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp_start: datetime = Field(default_factory=datetime.now)

class RuntimeConfig(BaseModel):
    """
    Configuración del runtime de Cerebellum.
    """
    max_messages: int = 10000
    idle_grace_ms: int = 50
