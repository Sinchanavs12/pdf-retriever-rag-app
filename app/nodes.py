
from .retriever import retrieve_chunks
from .generator import generate_answer

def retrieve_node(state):
    # Get the user's question
    question = state["question"]

    # Retrieve relevant chunks from ChromaDB
    results = retrieve_chunks(question, top_k=3)

    # Combine retrieved documents into context
    context = "\n\n".join(results["documents"][0])

    # Extract source information
    sources = []

    for metadata in results["metadatas"][0]:
        source = {
            "source": metadata["source"],
            "page_number": metadata["page_number"]
        }

        if source not in sources:
            sources.append(source)

    # Return updated state
    return {
        "context": context,
        "sources": sources
    }
def generate_node(state):
    # Get the user's question
    question = state["question"]

    # Get the retrieved PDF context
    context = state["context"]

    # Generate an answer using the LLM
    answer = generate_answer(question, context)

    # Return the generated answer
    return {
        "answer": answer
    }

