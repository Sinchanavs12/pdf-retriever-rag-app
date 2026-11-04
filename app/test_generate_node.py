
from .nodes import retrieve_node, generate_node

# Initial state
state = {
    "question": "What is symmetric encryption?",
    "context": "",
    "answer": "",
    "sources": []
}

# Step 1: Retrieve relevant PDF chunks
state.update(retrieve_node(state))

# Step 2: Generate an answer
state.update(generate_node(state))

print("Question:", state["question"])
print("\nGenerated Answer:")
print(state["answer"])
print("\nSources:")
print(state["sources"])

print("\nGenerate node test successful!")