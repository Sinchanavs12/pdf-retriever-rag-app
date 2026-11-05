
from app.retriever import retrieve_chunks

question = "What is symmetric encryption?"

results = retrieve_chunks(question, top_k=3)

print("Question:", question)
print("\nRetrieved results:\n")

for i, document in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]

    print(f"Result {i + 1}")
    print("Source:", metadata["source"])
    print("Page:", metadata["page_number"])
    print("Distance:", distance)
    print("Content:", document)
    print("-" * 60)
