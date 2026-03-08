"""
Environment implementations.

Each class represents a different type of world context
the cognitive agent can operate in.

Available environments
----------------------
TextEnvironment          : Plain-text static context (dev/testing).
SystemPromptEnvironment  : LLM-style system prompt + constraints.
KnowledgeBaseEnvironment : In-memory knowledge base / document store (RAG placeholder).
APIEnvironment           : External API as environment state source.
"""

from .text_environment import TextEnvironment
from .system_prompt_environment import SystemPromptEnvironment
from .knowledge_base_environment import KnowledgeBaseEnvironment
from .api_environment import APIEnvironment

__all__ = [
    "TextEnvironment",
    "SystemPromptEnvironment",
    "KnowledgeBaseEnvironment",
    "APIEnvironment",
]
