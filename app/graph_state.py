
from typing import TypedDict, List, Dict, Any


class GraphState(TypedDict):
    question: str
    context: str
    answer: str
    sources: List[Dict[str, Any]]
