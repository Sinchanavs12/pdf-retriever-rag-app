
from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):

    # Extract text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    # Convert text into numerical vectors
    embeddings = model.encode(texts)

    return embeddings