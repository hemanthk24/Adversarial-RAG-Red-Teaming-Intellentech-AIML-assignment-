# Adversarial RAG Red-Teaming

### Intellentech AI/ML Assignment

An end-to-end Retrieval-Augmented Generation (RAG) application built
with LangChain, LangGraph, Pinecone, BM25, MMR, OpenAI, and Streamlit.

The project evaluates three RAG failure modes:

-   Hallucination
-   Wrong citation / source attribution
-   Self-contradiction

The knowledge base is a deliberately messy fictional healthcare dataset
containing contradictory versions, outdated documents, near-duplicate
distractors, and irrelevant noise documents.

------------------------------------------------------------------------

## 1. Project Overview

The application is based on the fictional **BasicCare Health & Wellness
Handbook**.

For every user question, the RAG pipeline:

1.  Retrieves relevant document chunks.
2.  Passes retrieved content and metadata to the generation model.
3.  Generates an evidence-grounded answer.
4.  Returns only the source documents that directly support the answer.
5.  Exposes retrieved evidence for inspection in the Streamlit UI.

A separate red-team harness runs adversarial questions against the same
LangGraph workflow and evaluates whether failures occurred.

> **Note:** This is a fictional educational RAG demonstration and is not
> intended to provide real medical advice.

------------------------------------------------------------------------

## 2. Main Features

-   LangGraph-based RAG workflow
-   Pinecone vector retrieval
-   BM25 keyword retrieval
-   Hybrid retrieval using `EnsembleRetriever`
-   MMR retrieval
-   Metadata-aware generation
-   Structured citation output
-   Streamlit continuous chat interface
-   Retrieved evidence inspection
-   Automated/semi-automated red-team evaluation
-   Hallucination detection
-   Wrong-citation detection
-   Self-contradiction detection
-   False-positive and false-negative analysis
-   Baseline vs after-fix comparison

------------------------------------------------------------------------

## 3. Knowledge Base

The project contains **16 short documents**.

The dataset was deliberately engineered to make retrieval and source
attribution challenging.

### Contradictory pairs

-   Fever Guidelines --- Version 1 / Version 2
-   Hydration Guidelines --- Version 1 / Version 2
-   Minor Burn Care --- Version 1 / Version 2

### Outdated documents

-   Hydration Guidelines Version 1
-   Sleep Guidelines 2024

### Near-duplicate distractors

-   General Exercise vs Workplace Exercise
-   General Hand Hygiene vs Healthcare Setting Hand Hygiene

### Normal documents

-   Headache & Rest Guidelines
-   Common Cold & Self-Care

### Irrelevant noise

-   Photography Basics
-   Computer Troubleshooting

------------------------------------------------------------------------

## 4. Architecture

### Baseline

``` text
User Question
     |
     v
Semantic Retrieval
     |
     v
Top-K Chunks
     |
     v
Generation LLM
     |
     +----------+
     |          |
     v          v
  Answer    Citations
```

### Updated configuration

``` text
                         User Question
                              |
                 +------------+------------+
                 |                         |
                 v                         v
          Pinecone + MMR                 BM25
          Semantic Retrieval         Keyword Retrieval
                 |                         |
                 +------------+------------+
                              |
                              v
                       EnsembleRetriever
                              |
                              v
                       Relevant Chunks
                              |
                              v
                     Metadata + Content
                              |
                              v
                            GPT-4o
                              |
                       +------+------+
                       |             |
                       v             v
                     Answer      Citations
```

The Streamlit frontend displays the generated answer, supporting
citations, and retrieved evidence.

------------------------------------------------------------------------

## 5. Repository Structure

The repository is organized around the RAG application, red-team evaluation, failure analysis, and supporting results.

```text
Intellentech project/
│
├── data/
│   └── documents / knowledge-base files
│
├── evaluation/
│   └── evaluation-related files
│
├── failure_analysis/
│   ├── failure_analysis.ipynb
│   └── failure_analysis.md
│
├── intlt/
│   └── supporting project files
│
├── rag/
│   ├── graph/
│   │   └── LangGraph state, nodes and workflow
│   │
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_loader.py
│   ├── embeddings.py
│   ├── metadata_and_datapaths.py
│   └── retriever.py
│
├── red_team/
│   ├── detector.py
│   ├── run_tests.py
│   ├── schemas.py
│   └── test_cases.py
│
├── research/
│   └── research / supporting material
│
├── results/
│   ├── after_update_red_team_test_results_summary.csv
│   ├── after_update_red_team_test_results.csv
│   ├── baseline_red_team_test_results_summary.csv
│   ├── baseline_red_team_test_results.csv
│   ├── failure_summary.json
│   └── updated_failure_summary.json
│
├── .env
├── .env_example
├── .gitignore
├── .python-version
├── app.py
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Main folders

| Folder / File | Purpose |
|---|---|
| `data/` | Knowledge-base documents used by the RAG system |
| `evaluation/` | Evaluation-related project material |
| `failure_analysis/` | Detailed baseline/after-fix failure analysis |
| `rag/` | Core RAG implementation |
| `rag/graph/` | LangGraph state, nodes and compiled workflow |
| `red_team/` | Adversarial tests and failure detectors |
| `research/` | Supporting research and project material |
| `results/` | Baseline and updated red-team outputs and evaluation summaries |
| `app.py` | Streamlit frontend |
| `main.py` | Main project entry/supporting execution file |
| `pyproject.toml` | Python project configuration |
| `requirements.txt` | Python dependencies |
| `.env_example` | Example environment-variable configuration |
| `README.md` | Project setup, usage, evaluation and post-mortem documentation |

> **Security note:** `.env` contains local secrets/API keys and should not be committed to the repository. Only `.env_example` should be shared.

## 6. Requirements

Recommended environment:

-   Python 3.10+
-   OpenAI API access
-   Pinecone account/API access
-   Internet connection for external APIs and model downloads where
    required

Python dependencies are listed in:

``` text
requirements.txt
```

------------------------------------------------------------------------

## 7. Installation

Clone the repository:

``` bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

Create a virtual environment.

### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 8. Environment Variables

Create a `.env` file in the project root:

``` env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
NVIDIA_API_KEY=your_nvidia_api_key
```

Do not commit `.env` to the repository.

Add it to `.gitignore`:

``` text
.env
```

If the final embedding implementation requires additional environment
variables, document them here.

------------------------------------------------------------------------

## 9. Pinecone Setup

The application uses the Pinecone index:

``` text
basiccare-guidelines
```

The Pinecone index dimension must match the embedding model used by the
repository.

The document chunks must be indexed before querying the application if
the final repository does not automatically perform ingestion.

------------------------------------------------------------------------

## 10. Run the Streamlit Application

Start the application with:

``` bash
streamlit run app.py
```

The application provides a continuous chat interface.

For each response, the UI displays:

``` text
Generated Answer
       |
       v
Supporting Sources
       |
       v
Retrieved Evidence
```

The **Retrieved Evidence** section can be expanded to inspect the chunks
and metadata supplied to the generation stage.

------------------------------------------------------------------------

## 11. LangGraph State

The RAG state is:

``` python
class RAGState(TypedDict):

    question: str

    retrieved_docs: List[Document]

    answer: str

    citations: List[str]
```

The main graph is:

``` text
START
  |
  v
Retrieve
  |
  v
Generate
  |
  v
END
```

The compiled workflow is used by both the Streamlit application and the
red-team harness.

------------------------------------------------------------------------

## 12. Retrieval

### Baseline retrieval

The baseline used semantic similarity retrieval from Pinecone.

``` text
Question
   |
Embedding
   |
Pinecone
   |
Top-K chunks
```

### Updated retrieval

The updated configuration combines Pinecone semantic retrieval and BM25
keyword retrieval.

The ensemble weights are:

``` python
weights = [0.8, 0.2]
```

The Pinecone retriever uses MMR:

``` python
search_kwargs = {
    "k": 3,
    "fetch_k": 8,
    "lambda_mult": 0.5
}
```

BM25 uses:

``` python
bm25_retriever.k = 3
```

The purpose of hybrid retrieval is to combine semantic relevance with
exact keyword matching for context-sensitive terms such as `workplace`,
`healthcare`, `general`, `version`, `2024`, and `2026`.

------------------------------------------------------------------------

## 13. Chunking

### Baseline

``` text
chunk_size = 300
chunk_overlap = 50
```

### Updated

``` text
chunk_size = 400
chunk_overlap = 60
```

The larger chunks were intended to preserve more surrounding context and
reduce the possibility of separating useful contextual information
across small chunks.

------------------------------------------------------------------------

## 14. Metadata-Aware Generation

The generation model receives both document content and metadata.

Relevant metadata includes:

-   Document ID
-   Topic
-   Version
-   Effective date
-   Scope/context

The generation instructions require the model to:

-   Use only retrieved evidence.
-   Check document metadata.
-   Match the source context to the question.
-   Avoid mixing different contexts unless explicitly asked to compare
    them.
-   Consider version and effective date.
-   Identify genuine conflicts.
-   Avoid unsupported claims.
-   Say when evidence is insufficient.
-   Cite only documents that directly support the answer.

------------------------------------------------------------------------

## 15. Citation Handling

The generation output uses structured citations containing:

``` text
doc_id
version
```

The LLM is instructed to select only sources that directly support the
final answer.

It should not cite every document simply because the document was
retrieved.

Conceptually:

``` text
Retrieved Documents
        |
        v
Metadata + Content
        |
        v
      GPT-4o
        |
        +-------------+
        |             |
        v             v
      Answer       Citations
```

------------------------------------------------------------------------

# 16. Red-Team Harness

The red-team harness is intentionally separate from the RAG application.

The RAG application is treated as the **system under test**.

The red-team harness sends adversarial questions to the compiled
workflow and evaluates the responses.

``` text
Red-Team Questions
        |
        v
LangGraph RAG
        |
        v
Answer + Evidence + Citations
        |
        v
Failure Detector
        |
        v
Evaluation Results
```

------------------------------------------------------------------------

## 17. Adversarial Test Distribution

The evaluation contains 25 tests:

  Failure Mode            Tests
  -------------------- --------
  Hallucination              10
  Wrong Citation             10
  Self-Contradiction          5
  **Total**              **25**

------------------------------------------------------------------------

## 18. Hallucination Evaluation

A hallucination test asks for information that is not supported by the
retrieved evidence.

The detector checks:

> Does the answer contain factual claims that are unsupported by the
> retrieved evidence?

Example:

``` text
Retrieved evidence:
No thermometer brand is mentioned.

Question:
What thermometer brand does BasicCare recommend?

Bad answer:
BasicCare recommends Braun.

Result:
Hallucination
```

If the model says that the available evidence is insufficient, that is
not considered a hallucination.

------------------------------------------------------------------------

## 19. Wrong-Citation Evaluation

Wrong-citation tests check whether the source cited by the model
actually supports the answer.

Example:

``` text
D09 → General Exercise
D10 → Workplace Exercise
```

Question:

``` text
What warm-up duration is recommended for workplace exercise?
```

The citation should correspond to the source that actually supports the
workplace-specific claim.

A wrong citation can occur even when the answer itself appears
reasonable.

The evaluation asks:

``` text
Question
   +
Answer
   +
Cited Source
   |
   v
Does the cited source support the claim?
```

------------------------------------------------------------------------

## 20. Self-Contradiction Evaluation

Self-contradiction tests use pairs of related questions.

``` text
Question 1
    |
    v
Answer 1

Question 2
    |
    v
Answer 2

Answer 1
   VS
Answer 2
```

The detector checks whether the answers make materially conflicting
claims about the same underlying fact.

Different answers are not automatically contradictions.

For example:

``` text
Version 1 → Recommendation A
Version 2 → Recommendation B
```

may be legitimate if the questions explicitly ask about different
versions.

Similarly:

``` text
General Exercise
       vs
Workplace Exercise
```

may legitimately have different recommendations.

Therefore the detector must consider context, version, date, and scope
before declaring a contradiction.

------------------------------------------------------------------------

## 21. `flagged` vs `actual_failure`

The evaluation uses two separate fields.

### `flagged`

Whether the automated detector identified a failure.

### `actual_failure`

Whether manual evaluation confirmed that the RAG system actually failed.

This is necessary because the detector itself can make mistakes.

The four possible outcomes are:

  Actual Failure   Detector Flag   Meaning
  ---------------- --------------- ----------------
  True             True            True Positive
  True             False           False Negative
  False            True            False Positive
  False            False           True Negative

For the current small evaluation set, manual verification is used to
establish `actual_failure`.

------------------------------------------------------------------------

## 22. Run the Red-Team Harness

Run:

``` bash
python red_team/run_tests.py
```

The test results are written to:

``` text
results/red_team_test_results.csv
```

The result file records information such as:

``` text
test_id
mode
question
answer
citations
retrieved_docs
flagged
confidence
judge_reason
actual_failure
notes
```

------------------------------------------------------------------------

## 23. Run Evaluation

After the red-team tests complete:

``` bash
python main.py
```

The evaluation summary is written to:

``` text
results/failure_summary.json
```

The evaluation calculates:

-   Total tests
-   Actual failures
-   Failure rate
-   Detector flags
-   True positives
-   False positives
-   False negatives
-   True negatives
-   Precision
-   Recall
-   False positive rate
-   False negative rate
-   Specificity
-   Accuracy

------------------------------------------------------------------------

# 24. Baseline Evaluation Results

The baseline RAG system was evaluated using the same 25 adversarial test cases before applying the targeted update.

## 24.1 Test Distribution

| Failure Mode | Number of Tests |
|---|---:|
| Hallucination | 10 |
| Wrong Citation | 10 |
| Self-Contradiction | 5 |
| **Total** | **25** |

## 24.2 Baseline Failure Rates

| Failure Mode | Total Tests | Actual Failures | Failure Rate | Detector Flags |
|---|---:|---:|---:|---:|
| Hallucination | 10 | 0 | 0% | 0 |
| Wrong Citation | 10 | 1 | 10% | 4 |
| Self-Contradiction | 5 | 0 | 0% | 1 |
| **Overall** | **25** | **1** | **4%** | **5** |

The baseline system had **1 confirmed failure out of 25 tests**, giving an observed failure rate of **4%**. The confirmed failure occurred in the wrong-citation category.

## 24.3 Baseline Detector Performance

| Metric | Hallucination | Wrong Citation | Self-Contradiction | Overall |
|---|---:|---:|---:|---:|
| Total Tests | 10 | 10 | 5 | 25 |
| Actual Failures | 0 | 1 | 0 | 1 |
| Detector Flags | 0 | 4 | 1 | 5 |
| True Positives | 0 | 1 | 0 | 1 |
| False Positives | 0 | 3 | 1 | 4 |
| False Negatives | 0 | 0 | 0 | 0 |
| True Negatives | 10 | 6 | 4 | 20 |
| Accuracy | 100% | 70% | 80% | **84%** |
| Specificity | 100% | 66.67% | 80% | **83.33%** |

### Baseline Interpretation

The detector correctly identified the confirmed C02 failure, but it also produced several false positives. Therefore, the baseline evaluation contained:

- **1 true positive**
- **4 false positives**
- **0 false negatives**
- **20 true negatives**

The main observed RAG failure was the wrong citation in C02.

---

# 25. Baseline Failure: C02

## Test Information

```text
Test ID: C02
Failure Mode: wrong_citation
flagged = True
actual_failure = True
```

The test targeted the difference between:

```text
D09 → General Exercise
D10 → Workplace Exercise
```

Both documents discuss exercise and are therefore semantically similar, but the question specifically targeted the workplace context.

### What Went Wrong?

The baseline system could retrieve information from both similar documents and mix information between the contexts during answer generation and citation selection.

This resulted in incorrect source attribution.

### Root Cause

The observed root cause was:

> **Context/source attribution confusion between similar documents.**

The baseline generation process did not explicitly require the model to check the document context, scope, version, and effective date before selecting evidence and citations.

---

# 26. Baseline False Positives

The baseline detector also produced false positives.

### C07

The detector flagged C07, but manual evaluation determined that the requested 2024 source was appropriate.

```text
flagged = True
actual_failure = False
```

Therefore, C07 was a false positive.

### C09 and C10

C09 and C10 were also flagged by the detector but were not confirmed as actual citation failures during manual verification.

### SC04

SC04 was flagged as a self-contradiction, but manual evaluation determined that the difference was caused by different contexts:

```text
D09 → General Exercise
D10 → Workplace Exercise
```

Different context-specific recommendations do not automatically represent a contradiction.

### Baseline Detector Summary

```text
Actual failures   = 1
False positives   = 4
False negatives   = 0
True negatives    = 20
```

---

# 27. Targeted Update

After analyzing the baseline failure, the RAG pipeline was updated to improve **context-aware retrieval and generation**.

The update included:

1. Chunk size `300 → 400`
2. Chunk overlap `50 → 60`
3. Hybrid semantic + BM25 retrieval
4. MMR retrieval
5. Controlled retrieval context
6. Metadata-aware generation
7. More precise generation instructions
8. Structured citation selection

These changes were treated as one combined targeted intervention focused on reducing the source-attribution problem observed in C02.

## 27.1 Configuration Comparison

| Component | Baseline | Updated |
|---|---|---|
| Chunk Size | 300 | 400 |
| Chunk Overlap | 50 | 60 |
| Retrieval | Semantic | Hybrid |
| Keyword Retrieval | Not used | BM25 |
| Semantic Selection | Similarity | MMR |
| Pinecone `k` | Baseline configuration | 3 |
| MMR `fetch_k` | Not used | 8 |
| MMR `lambda_mult` | Not used | 0.5 |
| BM25 `k` | Not used | 3 |
| Generation Prompt | Basic evidence prompt | Metadata-aware prompt |
| Citation Handling | Retrieved-source handling | Structured citation selection |

---

# 28. Chunking, Retrieval and Generation Changes

## 28.1 Chunking

### Baseline

```text
chunk_size = 300
chunk_overlap = 50
```

### Updated

```text
chunk_size = 400
chunk_overlap = 60
```

The larger chunks were intended to preserve more surrounding context such as section information, recommendations, explanations, and scope.

## 28.2 Hybrid Retrieval

The updated system combines Pinecone semantic retrieval with BM25 keyword retrieval.

```text
                User Question
                     |
          +----------+----------+
          |                     |
          v                     v
      Pinecone                 BM25
      Semantic                Keyword
      Retrieval              Retrieval
          |                     |
          +----------+----------+
                     |
                     v
             EnsembleRetriever
```

The ensemble uses:

```python
weights = [0.8, 0.2]
```

This gives greater weight to semantic retrieval while allowing BM25 to contribute exact keyword matching.

BM25 is useful for context-specific terms such as:

```text
workplace
healthcare
general
2024
2026
version
```

## 28.3 MMR Retrieval

The Pinecone retriever was changed to MMR retrieval.

```python
search_kwargs = {
    "k": 3,
    "fetch_k": 8,
    "lambda_mult": 0.5
}
```

MMR considers both relevance to the query and diversity among selected results. This can reduce redundant chunks when multiple documents contain similar information.

## 28.4 Metadata-Aware Generation

The generation model receives metadata together with retrieved content, including information such as:

- Document ID
- Topic
- Scope / Context
- Version
- Effective Date

The updated prompt instructs the model to:

1. Use only retrieved evidence.
2. Check document metadata.
3. Match the source context to the question.
4. Check version and effective date.
5. Avoid mixing different contexts.
6. Identify genuine conflicts.
7. Avoid unsupported claims.
8. Say when evidence is insufficient.
9. Cite only documents that directly support the answer.

## 28.5 Structured Citation Handling

The generation model returns structured citation information containing:

```text
doc_id
version
```

The model is instructed to cite only documents that directly support the final answer and to use the exact document ID and version from the retrieved evidence.

---

# 29. After-Update Evaluation Results

After applying the targeted update, the **same 25 adversarial tests** were executed again.

## 29.1 After-Update Failure Rates

| Failure Mode | Total Tests | Actual Failures | Failure Rate | Detector Flags |
|---|---:|---:|---:|---:|
| Hallucination | 10 | 0 | 0% | 0 |
| Wrong Citation | 10 | 0 | 0% | 1 |
| Self-Contradiction | 5 | 0 | 0% | 0 |
| **Overall** | **25** | **0** | **0%** | **1** |

After the update, no actual failures were confirmed in the 25-test evaluation set.

## 29.2 After-Update Detector Performance

| Metric | Hallucination | Wrong Citation | Self-Contradiction | Overall |
|---|---:|---:|---:|---:|
| Total Tests | 10 | 10 | 5 | 25 |
| Actual Failures | 0 | 0 | 0 | 0 |
| Detector Flags | 0 | 1 | 0 | 1 |
| True Positives | 0 | 0 | 0 | 0 |
| False Positives | 0 | 1 | 0 | 1 |
| False Negatives | 0 | 0 | 0 | 0 |
| True Negatives | 10 | 9 | 5 | 24 |
| Accuracy | 100% | 90% | 100% | **96%** |
| Specificity | 100% | 90% | 100% | **96%** |

The remaining detector flag was manually classified as a false positive.

---

# 30. Before vs After Comparison

The same 25 adversarial tests were used before and after the update.

## 30.1 Overall Metrics

| Metric | Baseline | After Update | Change |
|---|---:|---:|---:|
| Total Tests | 25 | 25 | — |
| Actual Failures | **1** | **0** | -1 |
| Actual Failure Rate | **4%** | **0%** | **-4 percentage points** |
| Detector Flags | 5 | 1 | -4 |
| True Positives | 1 | 0 | -1 |
| False Positives | 4 | 1 | -3 |
| False Negatives | 0 | 0 | 0 |
| True Negatives | 20 | 24 | +4 |
| Detector Accuracy | **84%** | **96%** | **+12 percentage points** |
| Detector Specificity | **83.33%** | **96%** | **+12.67 percentage points** |

## 30.2 Failure-Mode Comparison

| Failure Mode | Baseline Actual Failures | Baseline Failure Rate | After Update Actual Failures | After Update Failure Rate |
|---|---:|---:|---:|---:|
| Hallucination | 0/10 | 0% | 0/10 | 0% |
| Wrong Citation | 1/10 | **10%** | 0/10 | **0%** |
| Self-Contradiction | 0/5 | 0% | 0/5 | 0% |
| **Overall** | **1/25** | **4%** | **0/25** | **0%** |

---

# 31. C02 Before vs After

C02 was the confirmed baseline failure and therefore the main test used to evaluate the targeted intervention.

## Before Update

```text
Test ID: C02
Mode: wrong_citation

flagged = True
actual_failure = True
```

The baseline system could mix information between:

```text
D09 → General Exercise
D10 → Workplace Exercise
```

This resulted in incorrect source attribution.

## After Update

```text
Test ID: C02
Mode: wrong_citation

flagged = False
actual_failure = False
```

The updated system correctly selected the workplace-specific source:

```text
D10 (Version 1.0)
```

The answer was therefore supported by the appropriate context-specific document.

---

# 32. Why Did the Results Change?

The improvement is attributed to the combined updated RAG configuration.

### 1. Larger Chunks

Changing from `300/50` to `400/60` provided more surrounding context inside retrieved chunks.

### 2. Hybrid Retrieval

BM25 added exact keyword matching alongside semantic retrieval. This is useful when context-specific words such as `workplace` are important.

### 3. MMR

MMR helped balance relevance and diversity and reduce redundant retrieval.

### 4. Controlled Retrieval Context

Passing a smaller set of relevant chunks to the generation stage reduced unnecessary similar evidence.

### 5. Metadata-Aware Generation

The LLM received metadata such as topic, context, version, and effective date and was explicitly instructed to check it before answering.

### 6. More Precise Prompting

The updated prompt explicitly instructed the model not to mix information from different contexts unless the question asks for a comparison.

### 7. Structured Citation Selection

The model was instructed to select only documents that directly support the final answer.

Together, these changes were intended to reduce the source-attribution problem identified in C02.

---

# 33. Important Experimental Limitation

Several related components were changed together.

Therefore, the experiment demonstrates the effect of the **combined targeted intervention** rather than proving that one individual change was solely responsible for the improvement.

The experiment does not isolate the individual contribution of:

- Chunking
- BM25
- MMR
- Retrieval size
- Prompting
- Metadata
- Citation handling

The reported 0% actual failure rate applies only to this 25-question engineered evaluation set.

---

# 34. Post-Mortem: Why This Red-Team Approach?

The red-team harness was kept separate from the RAG application so that
the RAG system remains the system under test.

The three failure modes were selected because they test different parts
of a RAG system:

``` text
Hallucination
    ↓
Can the model invent unsupported information?

Wrong Citation
    ↓
Can the system attribute a claim to the wrong source?

Self-Contradiction
    ↓
Can the system produce inconsistent answers to related questions?
```

An LLM-based structured detector was selected because these checks
require semantic comparison rather than only exact string matching.

For example, wrong-citation detection requires checking whether a cited
source actually supports a generated claim. Self-contradiction requires
understanding whether two different answers refer to the same underlying
fact or to different contexts/versions.

Manual verification was retained for the small current test set so that
detector mistakes could be separated from real RAG failures.

------------------------------------------------------------------------

# 35. Alternatives Considered

## Rule-Based Detection

A deterministic system could compare answers with expected values and
expected source IDs.

Advantages:

-   Deterministic
-   Cheap
-   Reproducible

Disadvantages:

-   Requires more hand-written rules
-   Less flexible for open-ended answers
-   More difficult to generalize

## Embedding-Based Evaluation

Generated answers could be compared with reference answers using
semantic similarity.

Advantages:

-   Automated
-   Scales better than manual comparison

Disadvantages:

-   Similar wording does not guarantee factual correctness
-   Does not directly establish citation correctness

## Dedicated RAG Evaluation Frameworks

A dedicated evaluation framework could provide additional retrieval and
generation metrics.

For this assignment, the custom detector was preferred because it
directly targets the three required failure modes and keeps the
implementation understandable.

------------------------------------------------------------------------

# 36. What Is Likely to Break at Larger Scale?

### Larger document collections

With thousands or millions of documents, simple top-K retrieval may
return many similar chunks.

A stronger production pipeline would likely require:

``` text
Retriever
   ↓
Reranker
   ↓
Context Filtering
   ↓
Generation
```

### More document versions

As the number of versions grows, version-aware retrieval becomes more
important.

### Larger red-team suites

Manual verification of `actual_failure` would not scale to thousands of
tests.

A larger evaluation system would need stronger ground truth, automated
scoring, sampling, and human audits.

### Larger contexts

Passing too many retrieved chunks to the LLM increases token usage and
can increase the chance of evidence mixing.

------------------------------------------------------------------------

# 37. One Practical Robustness Idea

A practical next improvement would be a **context-aware reranking
stage**.

The reranker could score each candidate using:

``` text
Query relevance
+
Topic match
+
Scope/context match
+
Version/date match
```

For example:

``` text
Question:
workplace exercise warm-up

D09:
General Exercise

D10:
Workplace Exercise
```

The reranker could give additional weight to the `workplace` context and
prioritize D10.

This would reduce the chance that a semantically similar but
contextually incorrect document reaches the generation stage.

------------------------------------------------------------------------

# 38. Submission Checklist

Before submitting:

-   [ ] `README.md`
-   [ ] `requirements.txt`
-   [ ] `.gitignore`
-   [ ] `.env` excluded from Git
-   [ ] 16 knowledge-base documents
-   [ ] `ground_truth.json`
-   [ ] Working Streamlit application
-   [ ] Working LangGraph workflow
-   [ ] Pinecone retrieval
-   [ ] Citations returned with answers
-   [ ] Retrieved evidence visible
-   [ ] Red-team questions
-   [ ] Red-team harness
-   [ ] CSV test results
-   [ ] Evaluation summary
-   [ ] Failure analysis
-   [ ] Baseline results
-   [ ] Targeted update
-   [ ] After-fix results
-   [ ] Before/after comparison
-   [ ] Clean-environment test
-   [ ] Supporting PDF report

------------------------------------------------------------------------

# 39. Quick Start

``` bash
# Create environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or, if using the project configuration
# pip install .

# Configure .env
# OPENAI_API_KEY=...
# PINECONE_API_KEY=...

# Start application
streamlit run app.py

# Run red-team tests
python red_team/run_tests.py

# Generate evaluation summary
python main.py
```

The project demonstrates the complete workflow:

``` text
Build RAG
   ↓
Run Baseline
   ↓
Red-Team
   ↓
Measure Failures
   ↓
Analyze Root Cause
   ↓
Apply Targeted Update
   ↓
Rerun Same Tests
   ↓
Compare Before vs After
```

The baseline produced **1 confirmed failure in 25 tests (4%)**. After
the combined targeted update, **0 confirmed failures were observed in
the same 25-test set (0%)**. Detector accuracy improved from **84% to
96%** and detector specificity improved from **83.33% to 96%**.
