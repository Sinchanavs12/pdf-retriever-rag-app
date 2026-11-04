
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