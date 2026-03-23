"""
Tests for cerebellum cognitive components: WorkingMemory, SemanticMemory.
"""

import pytest
import uuid
from unittest.mock import AsyncMock
from cerebellum.cognition.memory.working_memory import WorkingMemory
from cerebellum.cognition.memory.semantic_memory import SemanticMemory
from cerebellum.cognition.runtime.types import Message, CognitiveContext

@pytest.mark.asyncio
async def test_working_memory_on_message():
    wm = WorkingMemory()
    msg_id = str(uuid.uuid4())
    context = CognitiveContext(run_id="test-run")
    
    # Simular guardado
    store_msg = Message(
        id=msg_id,
        sender="test",
        receiver="memory.working",
        topic="memory.store",
        payload={"scope": "working", "key": "test_key", "value": "test_value"}
    )
    await wm.on_message(store_msg, context)
    
    # Verificar estado interno
    assert wm._state["test_key"] == "test_value"

@pytest.mark.asyncio
async def test_semantic_memory_on_message():
    sm = SemanticMemory()
    msg_id = str(uuid.uuid4())
    context = CognitiveContext(run_id="test-run")
    
    # Simular guardado
    store_msg = Message(
        id=msg_id,
        sender="test",
        receiver="memory.semantic",
        topic="memory.store",
        payload={"scope": "semantic", "key": "fact1", "value": "the sky is blue"}
    )
    await sm.on_message(store_msg, context)
    
    # Verificar estado interno
    assert sm.knowledge["fact1"] == "the sky is blue"

@pytest.mark.asyncio
async def test_working_memory_recall_flow():
    wm = WorkingMemory()
    wm._state["x"] = 123
    
    msg_id = str(uuid.uuid4())
    context = CognitiveContext(run_id="test-run")
    
    recall_msg = Message(
        id=msg_id,
        sender="test",
        receiver="memory.working",
        topic="memory.recall",
        payload={"scope": "working", "key": "x"}
    )
    
    # Mocking self.publish since WorkingMemory.on_message calls it
    wm.publish = AsyncMock()
    
    await wm.on_message(recall_msg, context)
    
    # Verificar que se publicó la respuesta
    wm.publish.assert_called_once()
    args, kwargs = wm.publish.call_args
    assert args[0] == "memory.available"
    assert args[1]["data"] == 123
    assert args[1]["found"] is True
