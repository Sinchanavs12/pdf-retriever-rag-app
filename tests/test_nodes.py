
from app.nodes import retrieve_node

# Initial state
state = {
    "question": "What is symmetric encryption?",
    "context": "",
    "answer": "",
    "sources": []
}

# Execute retrieve node
updated_state = retrieve_node(state)

print("Retrieved Context:")
print(updated_state["context"])

print("\nRetrieved Sources:")
print(updated_state["sources"])

print("\nRetrieve node test successful!")