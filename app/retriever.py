
import chromadb
from sentence_transformers import SentenceTransformer


# Load the same embedding model used during storage
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(question, top_k=3):

    # Connect to the existing ChromaDB database
    client = chromadb.PersistentClient(path="chroma_db")

    # Access the stored collection
    collection = client.get_collection(
        name="pdf_documents"
    )

    # Convert the question into an embedding
    question_embedding = model.encode(question)

    # Search for the most similar chunks
    results = collection.query(
        query_embeddings=[question_embedding.tolist()],
        n_results=top_k
    )

    return results


def retrieve_multiple_questions(questions, top_k=3):

    all_documents = []
    all_metadatas = []
    seen_chunks = set()

    for question in questions:

        if not question.strip():
            continue

        results = retrieve_chunks(question, top_k)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]

        for document, metadata, chunk_id in zip(
            documents, metadatas, ids
        ):

            if chunk_id not in seen_chunks:

                seen_chunks.add(chunk_id)
                all_documents.append(document)
                all_metadatas.append(metadata)

    return {
        "documents": all_documents,
        "metadatas": all_metadatas
    }