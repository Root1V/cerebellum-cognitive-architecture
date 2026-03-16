import pytest
from unittest.mock import AsyncMock, patch

from qdrant_client.http.models import PointStruct
from cerebellum.infraestructure.storage.db_episodic import MemoryEpisodicStorage


@pytest.mark.asyncio
async def test_episodic_storage_initialize():
    """Prueba la inicialización del backend vectorial con AsyncQdrantClient."""
    with patch("cerebellum.infraestructure.storage.db_episodic.AsyncQdrantClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        # Simula que get_collections devuelve una lista de colecciones
        mock_collections = AsyncMock()
        mock_collections.collections = []
        mock_client.get_collections = AsyncMock(return_value=mock_collections)
        
        mock_client.create_collection = AsyncMock()

        storage = MemoryEpisodicStorage(collection_name="test_integration", vector_size=128)
        await storage.initialize()

        # Verifica que se crea la colección cuando no existe
        mock_client.get_collections.assert_called_once()
        mock_client.create_collection.assert_called_once()
        args, kwargs = mock_client.create_collection.call_args
        assert kwargs["collection_name"] == "test_integration"
        assert kwargs["vectors_config"].size == 128


@pytest.mark.asyncio
async def test_episodic_storage_store_memory():
    """Prueba el almacenado de vectores usando upsert."""
    with patch("cerebellum.infraestructure.storage.db_episodic.AsyncQdrantClient") as mock_client_class:
        mock_client = mock_client_class.return_value
        mock_client.upsert = AsyncMock()

        storage = MemoryEpisodicStorage(vector_size=2)
        
        vector = [0.1, 0.9]
        await storage.store_memory(memory_id="123", vector=vector, payload={"key": "val"})

        mock_client.upsert.assert_called_once()
        args, kwargs = mock_client.upsert.call_args
        
        points = kwargs.get("points", [])
        assert len(points) == 1
        assert isinstance(points[0], PointStruct)
        assert points[0].id == "123"
        assert points[0].vector == vector
        assert points[0].payload == {"key": "val"}
