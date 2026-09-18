from rag.graph.workflow import workflow
import pandas as pd
from red_team.detector import structured_judge, structured_judge_contradiction
from red_team.test_cases import TEST_CASES
import os
from red_team.detector import detect_hallucination, detect_wrong_citation, detect_self_contradiction

# rag fubction to run the workflow
def run_rag(question):

    result = workflow.invoke({
        "question": question,
        "retrieved_docs": [],
        "answer": "",
        "citations": []
    })

    return result

# red team tests
def run_red_team_tests(test_cases, structured_judge):

    results = []

    for test in test_cases:

        # -----------------------------------
        # SELF-CONTRADICTION TEST
        # -----------------------------------
        if test["mode"] == "self_contradiction":

            q1 = test["questions"][0]
            q2 = test["questions"][1]

            result1 = run_rag(q1)
            result2 = run_rag(q2)

            evaluation = detect_self_contradiction(
                q1,
                result1["answer"],
                q2,
                result2["answer"],
                structured_judge_contradiction
            )

            results.append({
                "test_id": test["id"],
                "mode": test["mode"],

                "question": q1 + " || " + q2,

                "answer": (
                    "Q1: " + result1["answer"] +
                    "\n\nQ2: " + result2["answer"]
                ),

                "citations": (
                    str(result1["citations"]) +
                    " || " +
                    str(result2["citations"])
                ),

                "retrieved_docs": (
                   str(result1['retrieved_docs'])
                   +
                   "----------------------"
                   +
                  str(result2['retrieved_docs'])
                ),

                "flagged": evaluation.contradiction_detected,

                "confidence": evaluation.confidence,

                "judge_reason": evaluation.reason,

                # Manually verify later
                "actual_failure": None,

                "notes": ""
            })

        # -----------------------------------
        # NORMAL SINGLE-QUESTION TEST
        # -----------------------------------
        else:

            result = run_rag(test["question"])

            # Hallucination
            if test["mode"] == "hallucination":

                evaluation = detect_hallucination(
                    test["question"],
                    result["answer"],
                    result["retrieved_docs"],
                    structured_judge
                )

            # Wrong citation
            elif test["mode"] == "wrong_citation":

                evaluation = detect_wrong_citation(
                    test["question"],
                    result["answer"],
                    result["retrieved_docs"],
                    result["citations"],
                    structured_judge
                )

            results.append({
                "test_id": test["id"],
                "mode": test["mode"],
                "question": test["question"],
                "answer": result["answer"],
                "citations": result["citations"],

                "retrieved_docs": [
                    result['retrieved_docs']
                ],

                "flagged": evaluation.failure_detected,

                "confidence": evaluation.confidence,

                "judge_reason": evaluation.reason,

                # Manually verify later
                "actual_failure": None,

                "notes": ""
            })

    return results


if __name__ == "__main__":
    # Run the red team tests
    test_results = run_red_team_tests(TEST_CASES, structured_judge)

    # Save results to a CSV file
    df = pd.DataFrame(test_results)
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/after_update_red_team_test_results.csv", index=False)
    df_summary = df[['test_id','mode','citations','flagged','confidence','actual_failure','notes']]
    df_summary.to_csv("results/after_update_red_team_test_results_summary.csv", index=False)






