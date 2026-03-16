"""
Tests for cerebellum cognitive components: MemoryManager, WorkingMemory, SemanticMemory, MemoryStream.
Todos los tests usan mocks para evitar dependencias externas (Qdrant, etc).
"""

import pytest
from unittest.mock import patch, AsyncMock
from cerebellum.cognition.memory.manager import MemoryManager
from cerebellum.cognition.memory.working_memory import WorkingMemory
from cerebellum.cognition.memory.semantic_memory import SemanticMemory
from cerebellum.cognition.memory.memory_stream import MemoryStream


@pytest.mark.asyncio
async def test_memory_manager_remember_and_recall_with_mock():
    # Mockear EpisodicMemory para evitar acceso a Qdrant
    with patch("cerebellum.cognition.memory.manager.EpisodicMemory", autospec=True) as MockEpisodic:
        mock_epi = MockEpisodic.return_value
        mock_epi.store = AsyncMock()
        mock_epi.retrieve = AsyncMock(return_value={"goal": "bar", "result": 42, "timestamp": "now"})

        mm = MemoryManager()
        mm.episodic = mock_epi  # Forzar el mock
        await mm.remember("foo", {"goal": "bar", "result": 42, "timestamp": "now"})
        result = await mm.recall("foo", memory_type="episodic")
        assert result == {"goal": "bar", "result": 42, "timestamp": "now"}


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
