from dotenv import load_dotenv
from rag.graph.state import RAGState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()


# LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)


# -----------------------------
# Structured Output
# -----------------------------

class Citation(BaseModel):
    doc_id: str = Field(
        description="Exact document ID of the source that directly supports the answer."
    )

    version: str = Field(
        description="Exact version of the cited document."
    )


class RAGAnswer(BaseModel):
    answer: str = Field(
        description="Final answer based only on the retrieved evidence."
    )

    citations: list[Citation] = Field(
        default_factory=list,
        description="Only the documents that directly support the claims made in the answer."
    )


# Structured output LLM
structured_llm = llm.with_structured_output(RAGAnswer)


# -----------------------------
# Generate Node
# -----------------------------

def generate_node(state: RAGState):

    question = state["question"]
    docs = state["retrieved_docs"]

    # Build evidence with complete metadata
    context = "\n\n".join(
        [
            f"""
SOURCE DOCUMENT
Document ID: {doc.metadata.get('doc_id')}
Title: {doc.metadata.get('title')}
Topic: {doc.metadata.get('topic')}
Version: {doc.metadata.get('version')}
Effective Date: {doc.metadata.get('effective_date')}

CONTENT:
{doc.page_content}
"""
            for doc in docs
        ]
    )

    prompt = f"""
You are a careful evidence-grounded question-answering assistant.

Your task is to answer the user's question using ONLY the retrieved
documents provided below.

You must carefully inspect both the CONTENT and the METADATA of every
retrieved document before producing the answer.

IMPORTANT INSTRUCTIONS:

1. EVIDENCE ONLY
- Use only information explicitly supported by the retrieved documents.
- Do not use outside knowledge.
- Do not invent missing facts, numbers, dates, recommendations, brands,
  dosages, or other details.
- If the retrieved evidence is insufficient, clearly say that the
  available evidence is insufficient.

2. CHECK DOCUMENT METADATA
Before using a source, check:
- Document ID
- Topic
- Version
- Effective Date
- The context or scope described in the document

Do not treat all retrieved documents as interchangeable.

3. MATCH THE QUESTION'S CONTEXT
Identify the specific context requested by the question.

For example:
- "general exercise" should use general exercise guidance.
- "workplace exercise" should use workplace-specific guidance.
- "healthcare setting" should use healthcare-setting guidance.
- "2024 guideline" should use the 2024 document.
- "2026 guideline" should use the 2026 document.

Do NOT mix information from different contexts unless the question
explicitly asks for a comparison.

4. VERSION AND DATE
Pay attention to document version and effective date.

If the user explicitly asks about a particular version or year,
answer from that version when it is present in the retrieved evidence.

If multiple versions are retrieved:
- identify which version each claim comes from
- do not silently combine conflicting recommendations
- if they conflict, explicitly explain the conflict and identify
  the relevant documents

5. CONFLICT HANDLING
If two retrieved documents make different claims about the same topic:
- do not silently choose one
- determine whether the difference is caused by version, date,
  context, or scope
- if the documents genuinely conflict, state the conflict clearly
- cite the documents supporting each relevant claim

6. CITATIONS
Return ONLY citations that directly support the final answer.

Do NOT cite every retrieved document automatically.

For every citation:
- use the exact Document ID from the retrieved evidence
- use the exact Version from the retrieved evidence
- cite only a document that actually supports the answer

Do not cite a document merely because it was retrieved.

7. ANSWER QUALITY
Before finalizing your answer, internally check:

- Did I answer exactly what was asked?
- Is every factual claim supported by retrieved evidence?
- Did I use the correct document context?
- Did I check version and effective date?
- Did I accidentally mix general and context-specific information?
- Did I cite only the documents that support my answer?
- If evidence conflicts, did I explicitly mention the conflict?
- If evidence is insufficient, did I avoid guessing?

Do not show this internal checking process.
Return only the final answer and structured citations.

-----------------------------------
RETRIEVED EVIDENCE
-----------------------------------

{context}

-----------------------------------
USER QUESTION
-----------------------------------

{question}
"""

    response = structured_llm.invoke(prompt)

    citations = [
        f"{citation.doc_id} (Version {citation.version})"
        for citation in response.citations
    ]

    return {
        "answer": response.answer,
        "citations": citations
    }