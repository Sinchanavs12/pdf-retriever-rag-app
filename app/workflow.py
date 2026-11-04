
from langgraph.graph import StateGraph, START, END

from .graph_state import GraphState
from .nodes import retrieve_node, generate_node


# Create the graph
builder = StateGraph(GraphState)

# Register nodes
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)

# Define execution order
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

# Compile the graph
pdf_workflow = builder.compile()


def run_workflow(question):
    initial_state = {
        "question": question,
        "context": "",
        "answer": "",
        "sources": []
    }

    result = pdf_workflow.invoke(initial_state)

    return result
