
from .retriever import retrieve_chunks
from .generator import generate_answer

question = "What is symmetric encryption?"

# Retrieve relevant chunks from ChromaDB
results = retrieve_chunks(question, top_k=3)

# Combine retrieved chunks into one context
context = "\n\n".join(results["documents"][0])

# Generate an answer using Groq
answer = generate_answer(question, context)

print("Question:", question)
print("\nGenerated Answer:")
print(answer)