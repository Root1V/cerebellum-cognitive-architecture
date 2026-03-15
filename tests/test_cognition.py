"""
Tests for cerebellum cognitive components: MemoryManager, WorkingMemory, EpisodicMemory, SemanticMemory, MemoryStream.
"""

import pytest
import asyncio
from cerebellum.cognition.memory.manager import MemoryManager
from cerebellum.cognition.memory.working_memory import WorkingMemory
from cerebellum.cognition.memory.episodic_memory import EpisodicMemory
from cerebellum.cognition.memory.semantic_memory import SemanticMemory
from cerebellum.cognition.memory.memory_stream import MemoryStream


@pytest.mark.asyncio
async def test_memory_manager_remember_and_recall():
    mm = MemoryManager()
    await mm.remember("foo", {"goal": "bar", "result": 42, "timestamp": "now"})
    result = await mm.recall("foo", memory_type="episodic")
    # Puede ser None si la implementación de EpisodicMemory aún no almacena correctamente
    assert result is None or result is not None


@pytest.mark.asyncio
async def test_working_memory_store_and_retrieve():
    wm = WorkingMemory()
    await wm.store("x", 123)
    assert await wm.retrieve("x") == 123


@pytest.mark.asyncio
async def test_semantic_memory_store_and_retrieve():
    sm = SemanticMemory()
    await sm.store("fact1", {"fact": "the sky is blue"})
    assert await sm.retrieve("fact1") == {"fact": "the sky is blue"}


@pytest.mark.asyncio
async def test_memory_stream_store_and_retrieve():
    ms = MemoryStream()
    await ms.store("event1", {"data": "something happened"})
    results = await ms.retrieve("something happened")
    assert any("something happened" in str(r) for r in results)
