from typing import TypedDict, List
from langchain_core.documents import Document


class RAGState(TypedDict):
    question: str
    retrieved_docs: List[Document]
    answer: str
    citations: List[str]