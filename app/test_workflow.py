
from .workflow import run_workflow

question = "What is symmetric encryption?"

result = run_workflow(question)

print("Question:", result["question"])

print("\nGenerated Answer:")
print(result["answer"])

print("\nSources:")
print(result["sources"])

print("\nLangGraph workflow executed successfully!")