from langchain_openai import ChatOpenAI
from red_team.schemas import FailureEvaluation, ContradictionEvaluation

# llm for judging the answer
judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_judge = judge_llm.with_structured_output(
    FailureEvaluation
)

structured_judge_contradiction = judge_llm.with_structured_output(
    ContradictionEvaluation
)


#1. Hallucination detector
def detect_hallucination(question, answer, retrieved_docs, judge):

    evidence = "\n\n".join(
        [
            f"[{doc.metadata.get('doc_id')}] "
            f"{doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    prompt = f"""
    You are evaluating a RAG system for hallucination.

    Question:
    {question}

    Retrieved evidence:
    {evidence}

    RAG answer:
    {answer}

    Determine whether the answer contains claims that are not supported
    by the retrieved evidence.

    Important:
    - Do not use outside medical knowledge.
    - Judge only against the provided evidence.
    - If the evidence does not contain an answer and the system invents
    a specific fact, consider that unsupported.
    - If the answer correctly says that the evidence is insufficient,
    that is NOT a hallucination.

    Return the structured evaluation.
    """

    return judge.invoke(prompt)



# 2. Wrong-citation detector
def detect_wrong_citation(question, answer, retrieved_docs, citations, judge):

    evidence = "\n\n".join(
        [
            f"[{doc.metadata.get('doc_id')}, "
            f"Version {doc.metadata.get('version')}] "
            f"{doc.page_content}"
            for doc in retrieved_docs
        ]
    )

    citation_text = "\n".join(citations)

    prompt = f"""
    You are evaluating citation correctness in a RAG system.

    Question:
    {question}

    RAG answer:
    {answer}

    Cited sources:
    {citation_text}

    Retrieved evidence:
    {evidence}

    Determine whether the cited sources actually support the claims
    made in the answer.

    A citation is wrong if:
    1. The answer makes a factual claim, but the cited document does
       not support that claim.
    2. The cited document contradicts the claim.
    3. The cited document is not present in the retrieved evidence.

    Important:
    - Do NOT consider it a citation error simply because other
      retrieved documents were not cited.
    - Only evaluate the documents explicitly listed in the citations.
    - A citation is correct if the cited document directly supports
      the claim made in the answer.
    - Pay attention to document version when documents contain
      different versions of the same guideline.

    Return the structured evaluation.
    """

    return judge.invoke(prompt)


#3. Self-contradiction detector
def detect_self_contradiction(
    question1,
    answer1,
    question2,
    answer2,
    judge
):

    prompt = f"""
    You are evaluating whether a RAG system contradicts itself.

    Question 1:
    {question1}

    Answer 1:
    {answer1}

    Question 2:
    {question2}

    Answer 2:
    {answer2}

    Determine whether the two answers make materially conflicting
    claims about the same underlying fact.

    Important:
    - Different document versions may legitimately contain different
      values.
    - Do NOT call it a contradiction when the questions explicitly ask
      about different versions, dates, or contexts and the answers
      correctly reflect those differences.
    - Call it a contradiction when the system gives incompatible
      answers to the same underlying question without explaining the
      difference.
    - Do not call it a contradiction merely because the wording differs.

    Example of contradiction:

    Question 1: What temperature threshold should be used?
    Answer 1: 39.0°C

    Question 2: What temperature threshold should be used?
    Answer 2: 38.5°C

    If both answers are presented as the applicable current answer
    without explaining the difference, this is a contradiction.

    Example that is NOT necessarily a contradiction:

    Question 1: What did Version 1 say?
    Answer 1: 39.0°C

    Question 2: What did Version 2 say?
    Answer 2: 38.5°C

    These are different versions, so the different values can be
    legitimate.

    Return the structured evaluation.
    """

    return judge.invoke(prompt)