
from .retriever import retrieve_multiple_questions
from .generator import generate_answer
import re


def retrieve_node(state):
    question = state["question"]

    # Split a combined question into individual questions
    # Split combined questions using ?, . or !
    questions = [
        q.strip()
        for q in re.split(r'(?<=[.!?])\s+', question)
        if q.strip()
    ]

    # Retrieve relevant chunks separately for each question
    results = retrieve_multiple_questions(
        questions,
        top_k=8
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    # Prepare context with PDF filename and page number
    context_parts = []
    sources = []

    for document, metadata in zip(documents, metadatas):

        source_name = metadata.get("source", "Unknown PDF")
        page_number = metadata.get("page_number", "Unknown")

        context_parts.append(
            f"Source PDF: {source_name}\n"
            f"Page Number: {page_number}\n"
            f"Content:\n{document}"
        )

        # Collect unique source details
        source = {
            "source": source_name,
            "page_number": page_number
        }

        if source not in sources:
            sources.append(source)

    # Combine all retrieved chunks into one context
    context = "\n\n---\n\n".join(context_parts)

    # Debug information
    print(f"\nRetrieved unique chunks: {len(documents)}")

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        print(
            f"\nChunk {index} | "
            f"Source: {metadata.get('source', 'Unknown PDF')} | "
            f"Page: {metadata.get('page_number', 'Unknown')}"
        )
        print(document[:200])

    return {
        "context": context,
        "sources": sources
    }


def generate_node(state):
    question = state["question"]
    context = state["context"]

    # Generate an answer using the retrieved PDF context
    answer = generate_answer(question, context)

    return {
        "answer": answer
    }
