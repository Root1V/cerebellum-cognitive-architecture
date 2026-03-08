"""
Runtime components: main cognitive system loop and orchestration.

Environment implementations live in cerebellum.environment.
TextEnvironment is re-exported here for backward compatibility.
"""

from .cognitive_system import CognitiveSystem
from ..environment.text_environment import TextEnvironment  # backward compat

__all__ = [
    "CognitiveSystem",
    "TextEnvironment",  # deprecated: import from cerebellum.environment instead
]
