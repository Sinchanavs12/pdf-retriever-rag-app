
import chromadb
import os


def store_chunks(chunks, embeddings, collection_name="pdf_documents"):
    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(path="chroma_db")

    # Create or access the collection
    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Prepare data for storage
    ids = [
        f"{chunk['metadata']['source']}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    documents = [chunk["text"] for chunk in chunks]

    metadatas = [chunk["metadata"] for chunk in chunks]

    # Store chunks, embeddings, and metadata
    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas
    )

    return collection.count()
