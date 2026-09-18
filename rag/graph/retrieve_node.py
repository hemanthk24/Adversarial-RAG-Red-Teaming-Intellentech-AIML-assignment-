from rag.retirever import get_retriever
from rag.graph.state import RAGState

retriever = get_retriever()

# 1. retriever node
def retriever_node(state: RAGState):
    question = state['question']
    docs = retriever.invoke(question)
    return {
        "retrieved_docs":docs
    }
    