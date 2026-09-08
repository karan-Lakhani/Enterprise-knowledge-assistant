from src.document_loader import load_documents
from src.chunker import chunk_document
from src.embedder import generate_embeddings
from src.vector_store import store_chunks

documents = load_documents("documents")

all_chunks = []

for document in documents:
    all_chunks.extend(
        chunk_document(document)
    )

print(f"Total Chunks: {len(all_chunks)}")

embeddings = generate_embeddings(
    all_chunks
)

empty_chunks = 0

for chunk in all_chunks:

    if not chunk["text"].strip():
        empty_chunks += 1

print("\nEmpty Chunks:")
print(empty_chunks)

store_chunks(
    all_chunks,
    embeddings
)

print("Knowledge Base Created Successfully")