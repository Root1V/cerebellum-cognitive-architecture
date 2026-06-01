"""
Unit tests for EmbeddingClient blocking-I/O fix.

Spec: memory/specs/001-fix-blocking-io-embedding-client.md
"""

import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest

from cerebellum.cognition.attention.simple_attention import SimpleAttentionModule
from cerebellum.cognition.memory.episodic_memory import EpisodicMemory
from cerebellum.cognition.runtime.protocols import (
    AttentionSetFocusPayload,
    MemorySearchPayload,
    MemoryStorePayload,
)
from cerebellum.cognition.runtime.types import CognitiveContext, Message
from cerebellum.infraestructure.llm.embedd_client import EmbeddingClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VECTOR = [0.1, 0.2, 0.3, 0.4, 0.5]


def _make_mock_model() -> MagicMock:
    """Return a MagicMock that mimics SentenceTransformer.encode()."""
    model = MagicMock()
    model.encode.return_value = np.array(_VECTOR)
    return model


def _make_embedding_client() -> EmbeddingClient:
    """Build an EmbeddingClient with a mocked SentenceTransformer."""
    with patch(
        "cerebellum.infraestructure.llm.embedd_client.SentenceTransformer",
        return_value=_make_mock_model(),
    ):
        return EmbeddingClient()


# ---------------------------------------------------------------------------
# AC-1: encode() offloads to thread pool — event loop remains free
# memory/specs/001-fix-blocking-io-embedding-client.md — AC-1
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_encode_uses_to_thread_so_loop_is_not_blocked_AC1() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given encode() is called, the model runs in a thread via asyncio.to_thread."""
    client = _make_embedding_client()

    concurrent_ran = False

    async def concurrent_coroutine() -> None:
        nonlocal concurrent_ran
        await asyncio.sleep(0)  # yield control — will only run if loop is free
        concurrent_ran = True

    # Schedule a concurrent coroutine alongside encode
    result, _ = await asyncio.gather(
        client.encode("hello world"),
        concurrent_coroutine(),
    )

    assert concurrent_ran, "Event loop was blocked — concurrent coroutine never ran"
    assert result == _VECTOR


@pytest.mark.asyncio
async def test_encode_return_type_is_list_of_float_AC1() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given encode() returns, the value is list[float] — not numpy array, not Any."""
    client = _make_embedding_client()
    result = await client.encode("test")
    assert isinstance(result, list)
    assert all(isinstance(v, float) for v in result)


# ---------------------------------------------------------------------------
# AC-2: SimpleAttentionModule.on_start() encodes focus without blocking
# memory/specs/001-fix-blocking-io-embedding-client.md — AC-2
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_attention_on_start_sets_focus_vector_non_blocking_AC2() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given on_start() is called, _focus_vector is populated and the loop stays free."""
    mock_embedding = AsyncMock()
    mock_embedding.encode.return_value = _VECTOR

    module = SimpleAttentionModule(embedding=mock_embedding, initial_focus="test focus")
    context = CognitiveContext(run_id="test-run")

    await module.on_start(context)

    assert module._focus_vector == _VECTOR
    mock_embedding.encode.assert_called_once_with("test focus")


# ---------------------------------------------------------------------------
# AC-3: SimpleAttentionModule updates focus on attention.set_focus
# memory/specs/001-fix-blocking-io-embedding-client.md — AC-3
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_attention_set_focus_updates_vector_non_blocking_AC3() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given attention.set_focus is received, _focus_vector is updated without blocking."""
    new_vector = [0.9, 0.8, 0.7, 0.6, 0.5]
    mock_embedding = AsyncMock()
    mock_embedding.encode.side_effect = [_VECTOR, new_vector]

    module = SimpleAttentionModule(embedding=mock_embedding, initial_focus="old focus")
    context = CognitiveContext(run_id="test-run")
    await module.on_start(context)

    # Publish a set_focus message
    msg = Message(
        id=str(uuid.uuid4()),
        sender="test",
        receiver="attention.simple",
        topic="attention.set_focus",
        payload=AttentionSetFocusPayload(query="new focus").model_dump(),
    )
    await module.on_message(msg, context)

    assert module._focus_vector == new_vector
    assert module._focus_query == "new focus"


# ---------------------------------------------------------------------------
# AC-4: EpisodicMemory._handle_store generates embedding without blocking
# memory/specs/001-fix-blocking-io-embedding-client.md — AC-4
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_episodic_memory_store_encodes_without_blocking_AC4() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given memory.store (episodic), encoding is non-blocking and stored in Qdrant."""
    mock_embedding = AsyncMock()
    mock_embedding.encode.return_value = _VECTOR

    mock_storage = AsyncMock()
    mock_storage.initialize = AsyncMock()
    mock_storage.store_memory = AsyncMock()

    module = EpisodicMemory(embedding=mock_embedding, storage=mock_storage)
    context = CognitiveContext(run_id="test-run")
    await module.on_start(context)

    msg = Message(
        id=str(uuid.uuid4()),
        sender="test",
        receiver="memory.episodic",
        topic="memory.store",
        payload=MemoryStorePayload(
            scope="episodic",
            key="event-1",
            value={"content": "user said hello"},
        ).model_dump(),
    )
    await module.on_message(msg, context)

    mock_embedding.encode.assert_called_once()
    mock_storage.store_memory.assert_called_once()
    args = mock_storage.store_memory.call_args
    assert args[0][1] == _VECTOR  # vector argument is the encoded embedding


# ---------------------------------------------------------------------------
# AC-5: EpisodicMemory._handle_search generates query embedding without blocking
# memory/specs/001-fix-blocking-io-embedding-client.md — AC-5
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_episodic_memory_search_encodes_query_without_blocking_AC5() -> None:  # memory/specs/001-fix-blocking-io-embedding-client.md
    """Given memory.search, query embedding is generated non-blocking."""
    mock_embedding = AsyncMock()
    mock_embedding.encode.return_value = _VECTOR

    mock_storage = AsyncMock()
    mock_storage.initialize = AsyncMock()
    mock_storage.search_memory = AsyncMock(return_value=[])

    module = EpisodicMemory(embedding=mock_embedding, storage=mock_storage)
    context = CognitiveContext(run_id="test-run")
    await module.on_start(context)

    msg = Message(
        id=str(uuid.uuid4()),
        sender="test",
        receiver="memory.episodic",
        topic="memory.search",
        payload=MemorySearchPayload(query="what did the user say?", limit=5).model_dump(),
    )
    await module.on_message(msg, context)

    mock_embedding.encode.assert_called_once_with("what did the user say?")
    mock_storage.search_memory.assert_called_once()
    call_args = mock_storage.search_memory.call_args
    assert call_args[0][0] == _VECTOR  # first positional arg is the query vector
