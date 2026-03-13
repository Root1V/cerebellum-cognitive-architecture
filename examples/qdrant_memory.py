from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

def main():
        
    # modelo de embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # conectar a qdrant
    client = QdrantClient(host="localhost", port=6333)

    # crear colección
    client.recreate_collection(
        collection_name="documents",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

    # documentos
    texts = [
        "El gato duerme en el sofá",
        "Los perros son animales leales",
        "La inteligencia artificial está cambiando el mundo"
    ]

    # generar embeddings
    vectors = model.encode(texts)

    points = [
        PointStruct(
            id=i,
            vector=vectors[i].tolist(),
            payload={"text": texts[i]}
        )
        for i in range(len(texts))
    ]
    
    print("--- POINTS ---")
    for p in points:
        print(f"ID: {p.id}, Vector: {p.vector[:5]}..., Payload: {p.payload}")

    client.upsert(
        collection_name="documents",
        points=points
    )

    query = "animales domésticos"
    query_vector = model.encode(query)

    results = client.query_points(
        collection_name="documents",
        query=query_vector,
    )

    for point in results.points:
        print(point.payload["text"], point.score)
        
        
if __name__ == "__main__":
    main()
    
# --- POINTS ---
# ID: 0, Vector: [-0.02729421854019165, 0.04774963855743408, 0.03440946713089943, -0.012641239911317825, 0.01174915675073862]..., Payload: {'text': 'El gato duerme en el sofá'}
# ID: 1, Vector: [0.00987132266163826, 0.023180169984698296, 0.004640836268663406, -0.034508880227804184, 0.026659218594431877]..., Payload: {'text': 'Los perros son animales leales'}
# ID: 2, Vector: [-0.025516990572214127, 0.015104408375918865, -0.02979179657995701, -0.08501286804676056, 0.0009788938332349062]..., Payload: {'text': 'La inteligencia artificial está cambiando el mundo'}
# Los perros son animales leales 0.4909917
# La inteligencia artificial está cambiando el mundo 0.25865123
# El gato duerme en el sofá 0.2505472