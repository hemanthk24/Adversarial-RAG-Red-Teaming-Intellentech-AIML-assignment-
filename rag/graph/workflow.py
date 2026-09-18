from langgraph.graph import StateGraph, START, END
from rag.graph.state import RAGState
from rag.graph.retrieve_node import retriever_node
from rag.graph.generate_node import generate_node


# graph
graph = StateGraph(RAGState)

graph.add_node("retrieve", retriever_node)
graph.add_node("generate", generate_node)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

workflow = graph.compile()