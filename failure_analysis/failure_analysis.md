# Adversarial RAG — Baseline Failure Analysis and Targeted Fix

## 1. Overview

This document analyzes the performance of the Adversarial RAG system before and after applying a targeted improvement.

The objective was to identify and analyze:

- Hallucination failures
- Wrong-citation failures
- Self-contradiction failures
- False positives from the red-team detector
- False negatives
- Root causes of observed failures
- The effect of a targeted RAG improvement

The baseline evaluation was performed using **25 adversarial test cases**.

The evaluation distinguishes between:

- `flagged`: whether the automated red-team detector identified a failure.
- `actual_failure`: whether manual evaluation confirmed that the RAG system actually failed.

This distinction is important because the detector can incorrectly flag a correct response.

---

# 2. Baseline Test Distribution

The 25 tests were divided into three failure modes.

| Failure Mode | Tests |
|---|---:|
| Hallucination | 10 |
| Wrong Citation | 10 |
| Self-Contradiction | 5 |
| **Total** | **25** |

---

# 3. Baseline Results

## 3.1 Hallucination

| Metric | Result |
|---|---:|
| Total tests | 10 |
| Actual failures | 0 |
| Failure rate | 0% |
| Detector flagged | 0 |
| True positives | 0 |
| False positives | 0 |
| False negatives | 0 |
| True negatives | 10 |
| Accuracy | 100% |
| Specificity | 100% |

### Observation

No confirmed hallucination failures were observed in the 10 hallucination tests.

The RAG system either provided evidence-supported responses or appropriately indicated when the retrieved evidence was insufficient.

Therefore:

**Actual hallucination failure rate = 0%.**

This does not prove that the system can never hallucinate. It only means that no hallucination was observed in this particular baseline test set.

---

# 4. Baseline Wrong-Citation Evaluation

The wrong-citation category contained 10 tests.

| Metric | Result |
|---|---:|
| Total tests | 10 |
| Actual failures | 1 |
| Failure rate | 10% |
| Detector flagged | 4 |
| True positives | 1 |
| False positives | 3 |
| False negatives | 0 |
| True negatives | 6 |
| Precision | 25% |
| Recall | 100% |
| False Positive Rate | 33.33% |
| Specificity | 66.67% |
| Accuracy | 70% |

## Main Observation

One confirmed wrong-citation failure was found:

**C02**

The detector successfully identified this failure.

However, the detector also incorrectly flagged:

- C07
- C09
- C10

Therefore, the baseline wrong-citation detector produced several false alarms.

---

# 5. Confirmed Baseline Failure — C02

## Test ID

`C02`

## Failure Mode

`wrong_citation`

## Baseline Result

```text
flagged = True
actual_failure = True
````

## What Happened?

C02 targeted the difference between **general exercise guidance** and **workplace-specific exercise guidance**.

The knowledge base contains similar documents for these two contexts.

The baseline retrieval and generation process could retrieve information from both documents. Because the documents discuss the same general topic but have different contexts, the model could mix information between them when generating the answer and selecting citations.

This resulted in an incorrect source attribution.

## Root Cause

The primary observed root cause was **context/source attribution confusion** between similar documents.

The problem was not simply that the relevant document was absent. Instead, the system needed to better distinguish:

- Topic
- Document context
- Version
- Effective date
- Source scope

The baseline generation prompt did not provide sufficiently explicit instructions for checking these attributes before selecting evidence and citations.

---

# 6. Baseline Detector False Positives

The baseline system also produced false-positive detector results.

## C07

C07 was flagged by the detector, but manual evaluation determined that it was not an actual citation failure.

The requested information corresponded to the 2024 guideline, and the cited source was the appropriate document.

Therefore:

```text
flagged = True
actual_failure = False
```

This was a **false positive**.

## C09 and C10

C09 and C10 were also flagged by the detector but were not confirmed as actual citation failures.

The baseline detector was too aggressive when evaluating source/citation behavior around the requested guideline versions.

Therefore, these were also false positives.

Overall, the baseline wrong-citation category contained:

**1 actual failure + 3 false positives.**

---

# 7. Baseline Self-Contradiction Evaluation

| MetricResult     |     |
| ---------------- | --- |
| Total tests      | 5   |
| Actual failures  | 0   |
| Failure rate     | 0%  |
| Detector flagged | 1   |
| True positives   | 0   |
| False positives  | 1   |
| False negatives  | 0   |
| True negatives   | 4   |
| Accuracy         | 80% |
| Specificity      | 80% |

The baseline evaluation found no confirmed self-contradiction failures.

The detector produced one false positive.

The false positive occurred because some test cases intentionally contained different document contexts or versions.

Different recommendations do not automatically mean that the RAG system contradicted itself.

For example, general and workplace guidance can legitimately contain different recommendations because they apply to different contexts.

---

# 8. Baseline Overall Performance

| MetricBaseline       |        |
| -------------------- | ------ |
| Total tests          | 25     |
| Actual failures      | 1      |
| Actual failure rate  | **4%** |
| Detector flags       | 5      |
| True positives       | 1      |
| False positives      | 4      |
| False negatives      | 0      |
| True negatives       | 20     |
| Detector accuracy    | 84%    |
| Detector specificity | 83.33% |

The single confirmed failure was C02.

---

# 9. Targeted Fix

After analyzing the baseline failure, the RAG pipeline was modified to improve **context-aware retrieval and generation**.

The changes were focused on reducing confusion between similar documents, particularly the general-versus-workplace case observed in C02.

The targeted update included:

1. Larger chunks
2. Hybrid retrieval
3. MMR retrieval
4. Reduced retrieval context
5. Metadata-aware generation
6. More precise citation handling

---

# 10. Chunking Change

## Baseline

```text
chunk_size = 300
chunk_overlap = 50
```

## Updated

```text
chunk_size = 400
chunk_overlap = 60
```

The larger chunk size keeps more surrounding information together.

This helps preserve contextual information such as:

- Section context
- Recommendation
- Scope
- Supporting explanation

The overlap was also increased from 50 to 60 so that information near chunk boundaries is more likely to remain available in neighboring chunks.

The purpose of this change was to reduce the possibility of separating important contextual information across very small chunks.

---

# 11. Hybrid Retrieval

The updated system uses hybrid retrieval by combining semantic and keyword-based retrieval.

```text
User Question
      |
      +-------------------+
      |                   |
      v                   v
Pinecone MMR            BM25
Semantic Retrieval      Keyword Retrieval
      |                   |
      +---------+---------+
                |
                v
        EnsembleRetriever
```

The hybrid retriever combines:

- Pinecone semantic retrieval
- BM25 keyword retrieval

with the configured weights:

```python
weights = [0.8, 0.2]
```

The purpose of BM25 is to improve retrieval when exact terms are important.

This is particularly useful for context-specific questions containing terms such as:

- workplace
- healthcare
- general
- 2024
- 2026
- version

Semantic retrieval identifies conceptually similar documents, while keyword retrieval helps preserve important exact terms from the question.

---

# 12. MMR Retrieval

MMR was introduced on the Pinecone retriever.

The configuration used was:

```python
search_kwargs = {
    "k": 3,
    "fetch_k": 8,
    "lambda_mult": 0.5
}
```

MMR considers both:

- Relevance to the question
- Diversity among selected results

This helps reduce redundant retrieval when several chunks contain highly similar information.

This was useful for the deliberately messy knowledge base because multiple documents can discuss the same topic while applying to different contexts.

---

# 13. Retrieval Context

The updated pipeline was configured to provide a smaller retrieval context to the generation stage.

The purpose was to reduce unnecessary similar evidence being passed to the LLM while retaining enough relevant information to distinguish between related documents.

The updated retrieval flow was therefore:

```text
Question
   |
   v
Hybrid Retrieval
   |
   v
MMR
   |
   v
Relevant Chunks
   |
   v
Generation LLM
```

---

# 14. Metadata-Aware Generation

The generation prompt was made more precise.

Instead of providing only document content, the generation model receives document metadata together with the retrieved content.

The metadata includes information such as:

- Document ID
- Topic
- Version
- Effective Date
- Scope/context

Conceptually:

```text
SOURCE DOCUMENT

Document ID: D10
Topic: Exercise
Scope: Workplace
Version: 1.0
Effective Date: ...

CONTENT:
...
```

The generation model is explicitly instructed to inspect the metadata before using the retrieved evidence.

The updated prompt instructs the model to:

- Check the document ID
- Check the topic
- Check the context/scope
- Check the version
- Check the effective date
- Match the document context to the question
- Avoid mixing information from different contexts
- Identify genuine conflicts
- Avoid inventing unsupported information
- State when evidence is insufficient

This directly addresses the problem observed in C02.

---

# 15. Improved Generation Prompt

The updated generation prompt follows these principles:

```text
Use ONLY the retrieved evidence.

Before answering, carefully check the metadata and content of
the retrieved documents.

Check:
- Document ID
- Topic
- Scope/context
- Version
- Effective date

Match the source context to the user's question.

Do not mix information from different contexts unless the
question explicitly asks for a comparison.

If multiple documents contain conflicting information:
- identify the conflict
- determine whether the difference is related to version,
  date, context, or scope
- do not silently combine conflicting information

Do not invent facts.

If the evidence is insufficient, say so.

For citations:
- cite only documents that directly support the answer
- do not cite every retrieved document
- use the exact document ID
- use the exact document version
```

This gives the LLM a more explicit decision process for selecting the appropriate evidence.

---

# 16. Citation Handling Improvement

Citation generation was changed so that the structured LLM output selects the documents that directly support the final answer.

The citation schema contains:

```text
doc_id
version
```

The model is instructed to:

- Select only supporting sources
- Use the exact document ID
- Use the exact version
- Avoid citing documents simply because they were retrieved

The intended flow is:

```text
Retrieved Documents
        |
        v
Metadata + Content
        |
        v
      GPT-4o
        |
        +----------------+
        |                |
        v                v
      Answer          Citations
                       |
                       v
              Supporting Sources
```

This provides clearer traceability between the generated answer and the retrieved evidence.

---

# 17. Why the Fix Was Applied

The targeted baseline failure was C02.

The important issue was that the knowledge base contained documents with similar topics but different contexts.

For example:

```text
D09 → General Exercise
D10 → Workplace Exercise
```

Both documents are semantically related to exercise.

However, a question such as:

> What warm-up duration is recommended for workplace exercise?

requires the system to recognize that the **workplace context** is important.

The updated system addresses this through:

```text
Question
   |
   v
Semantic + Keyword Retrieval
   |
   v
MMR
   |
   v
Relevant Evidence
   |
   v
Metadata + Content
   |
   v
Context-Aware GPT-4o Generation
   |
   v
Supporting Citations
```

The goal was to make the system less likely to mix information from similar but contextually different documents.

---

# 18. After-Fix Results

The same 25 adversarial tests were rerun after the update.

## 18.1 Hallucination

| MetricAfter Fix |        |
| --------------- | ------ |
| Total tests     | 10     |
| Actual failures | 0      |
| Failure rate    | **0%** |
| Detector flags  | 0      |
| False positives | 0      |
| False negatives | 0      |
| True negatives  | 10     |
| Accuracy        | 100%   |
| Specificity     | 100%   |

No hallucination failures were observed after the update.

---

# 19. Wrong-Citation After-Fix Results

| MetricAfter Fix |        |
| --------------- | ------ |
| Total tests     | 10     |
| Actual failures | **0**  |
| Failure rate    | **0%** |
| Detector flags  | 1      |
| True positives  | 0      |
| False positives | 1      |
| False negatives | 0      |
| True negatives  | 9      |
| Specificity     | 90%    |
| Accuracy        | 90%    |

The previously confirmed C02 wrong-citation failure was not observed after the update.

The remaining detector flag was a false positive according to manual evaluation.

---

# 20. Self-Contradiction After-Fix Results

| MetricAfter Fix |        |
| --------------- | ------ |
| Total tests     | 5      |
| Actual failures | 0      |
| Failure rate    | **0%** |
| Detector flags  | 0      |
| True positives  | 0      |
| False positives | 0      |
| False negatives | 0      |
| True negatives  | 5      |
| Accuracy        | 100%   |
| Specificity     | 100%   |

No self-contradiction failures were observed after the update.

---

# 21. Before vs After

| MetricBaselineAfter Fix |        |        |
| ----------------------- | ------ | ------ |
| Total tests             | 25     | 25     |
| Actual failures         | **1**  | **0**  |
| Actual failure rate     | **4%** | **0%** |
| Detector flags          | 5      | 1      |
| True positives          | 1      | 0      |
| False positives         | 4      | 1      |
| False negatives         | 0      | 0      |
| True negatives          | 20     | 24     |
| Detector accuracy       | 84%    | 96%    |
| Detector specificity    | 83.33% | 96%    |

The overall actual failure rate decreased from **4% to 0%** on the tested adversarial set.

Detector flags decreased from **5 to 1**.

Detector accuracy increased from **84% to 96%**.

Detector specificity increased from **83.33% to 96%**.

---

# 22. C02 Before vs After

The most important comparison is C02.

## Before Fix

```text
Test: C02
Mode: wrong_citation

flagged = True
actual_failure = True
```

The system could mix information from the general and workplace exercise documents, resulting in incorrect source attribution.

## After Fix

```text
Test: C02
Mode: wrong_citation

flagged = False
actual_failure = False
```

The updated system selected the workplace-specific source:

```text
D10 (Version 1.0)
```

The answer was therefore supported by the appropriate context-specific document.

---

# 23. Why the Results Changed

The improvement is attributed to the combined updated RAG configuration.

### 1. Larger chunks

Changing:

```text
300 / 50
```

to:

```text
400 / 60
```

provided more surrounding context inside each chunk.

### 2. Hybrid retrieval

Combining semantic retrieval with BM25 improved the handling of exact context-specific terms such as "workplace".

### 3. MMR

MMR helped reduce redundant evidence and encouraged more diverse retrieved results.

### 4. Smaller generation context

Passing a smaller set of retrieved chunks reduced the amount of similar evidence available to the LLM to mix together.

### 5. Metadata-aware generation

The model was explicitly given document metadata such as topic, version, effective date, and context.

### 6. More precise generation instructions

The updated prompt explicitly required the model to check metadata and match the document context to the user's question.

### 7. Structured citation selection

The LLM was instructed to select only documents that directly support the final answer rather than automatically citing every retrieved document.

Together, these changes were intended to reduce the source-attribution problem identified in C02.

---

# 24. Limitations

The results should not be interpreted as proof that the RAG system is completely robust.

Several limitations remain:

1. The evaluation contains only 25 adversarial tests.
2. Manual verification is required to determine `actual_failure`.
3. The detector can still produce false positives.
4. The test documents are deliberately small and synthetic.
5. The observed 0% failure rate applies only to this particular test set.
6. The updated configuration combines several related changes, so the experiment does not isolate the individual contribution of chunking, hybrid retrieval, MMR, retrieval size, prompting, or citation handling.

Therefore, the results should be interpreted as an evaluation of the **updated RAG configuration as a whole**.

---

# 25. Conclusion

The baseline evaluation identified one confirmed failure in 25 adversarial tests.

The failure occurred in the wrong-citation category, specifically C02, where similar documents with different contexts could lead to incorrect source attribution.

The targeted update introduced:

- Larger chunks (`400` with `60` overlap)
- Hybrid semantic + keyword retrieval
- MMR retrieval
- Reduced retrieval context
- Metadata-aware generation
- More precise generation instructions
- Structured citation selection

The same 25 adversarial tests were then rerun.

The observed actual failure rate changed from:

**4% → 0%**

Detector flags changed from:

**5 → 1**

Detector accuracy changed from:

**84% → 96%**

Detector specificity changed from:

**83.33% → 96%**

Most importantly, the previously confirmed C02 wrong-citation failure was not observed after the update.

The results indicate that the updated retrieval and generation configuration improved performance on the engineered adversarial test set, particularly for distinguishing similar documents with different contexts.

However, because multiple components were changed together, the experiment demonstrates the effect of the **combined targeted intervention**, rather than proving that any single component was solely responsible for the improvement.

```
```
