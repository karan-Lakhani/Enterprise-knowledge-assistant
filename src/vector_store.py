import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="enterprise_knowledge"
)


def store_chunks(chunks, embeddings):

    collection.add(
        ids=[
            chunk["chunk_id"]
            for chunk in chunks
        ],

        documents=[
            chunk["text"]
            for chunk in chunks
        ],

        metadatas=[
            {
                "source": chunk["source"],
                "category": chunk["category"],
                "section_title": chunk["section_title"]
            }
            for chunk in chunks
        ],

        embeddings=embeddings.tolist()
    )