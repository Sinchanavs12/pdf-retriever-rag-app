import chromadb


def store_chunks(chunks, embeddings, document_id, collection_name="pdf_documents"):

    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(path="chroma_db")

    # Create or access the collection
    collection = client.get_or_create_collection(
        name=collection_name
    )

    # Generate unique IDs for every chunk
    ids = [
        f"{document_id}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    # Prepare documents
    documents = [chunk["text"] for chunk in chunks]

    # Add document_id to each chunk's metadata
    metadatas = []

    for chunk in chunks:
        metadata = chunk["metadata"].copy()
        metadata["document_id"] = document_id
        metadatas.append(metadata)

    # Store chunks, embeddings, and metadata
    collection.upsert(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=documents,
        metadatas=metadatas
    )

    # Return the number of chunks stored for this upload
    return len(ids)