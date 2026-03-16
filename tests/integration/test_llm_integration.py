import pytest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel

from cerebellum.infraestructure.llm.llm_client import LLMClient


class MockResponseOptions(BaseModel):
    content: str


class MockMessage(BaseModel):
    message: MockResponseOptions


class MockChatResponse(BaseModel):
    choices: list[MockMessage]


@pytest.mark.asyncio
async def test_llm_client_basic_integration():
    """Prueba que el cliente envia mensajes y procesa la respuesta base string."""
    with patch("axonium.LlamaAdapter.async_chat", new_callable=AsyncMock) as mock_chat:
        # Configura el mock para devolver una respuesta válida
        mock_response = MockChatResponse(
            choices=[MockMessage(message=MockResponseOptions(content="Hello world!"))]
        )
        mock_chat.return_value = mock_response

        client = LLMClient(model="test-model")
        result = await client.think(prompt="Say hello")

        assert result == "Hello world!"
        mock_chat.assert_called_once()
        args, kwargs = mock_chat.call_args
        # Verifica que el user message esté en el llamado al SDK
        assert kwargs["messages"][-1]["content"] == "Say hello"


@pytest.mark.asyncio
async def test_llm_client_structured_output():
    """Prueba de integración con salida tipada Pydantic."""
    class UserInfo(BaseModel):
        name: str
        age: int

    with patch("axonium.LlamaAdapter.async_chat", new_callable=AsyncMock) as mock_chat:
        # Devuelve JSON en formato válido para el modelo de Pydantic
        mock_response = MockChatResponse(
            choices=[MockMessage(message=MockResponseOptions(content='{"name": "Alice", "age": 30}'))]
        )
        mock_chat.return_value = mock_response

        client = LLMClient(model="test-model")
        result = await client.think(prompt="Extract data", output_model=UserInfo)

        assert isinstance(result, UserInfo)
        assert result.name == "Alice"
        assert result.age == 30
        
        # Debe solicitar JSON object al adaptador
        mock_chat.assert_called_once()
        _, kwargs = mock_chat.call_args
        assert kwargs.get("response_format") == {"type": "json_object"}
