from src.vector_store import collection
from src.embedder import model


def retrieve(query, top_k=5):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results