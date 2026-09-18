import pandas as pd
import json


def generate_failure_summary(
    csv_path="results/red_team_test_results.csv",
    json_path="results/updated_failure_summary.json"
):

    df = pd.read_csv(csv_path)

    # ---------------------------------
    # Convert values to boolean
    # ---------------------------------

    df["flagged"] = (
        df["flagged"]
        .astype(str)
        .str.lower()
        .eq("true")
    )

    df["actual_failure"] = (
        df["actual_failure"]
        .astype(str)
        .str.lower()
        .eq("true")
    )

    summary = {}

    # ---------------------------------
    # PER MODE EVALUATION
    # ---------------------------------

    for mode in [
        "hallucination",
        "wrong_citation",
        "self_contradiction"
    ]:

        mode_df = df[df["mode"] == mode]

        total_tests = len(mode_df)

        # -----------------------------
        # Confusion Matrix
        # -----------------------------

        tp = int(
            (
                (mode_df["flagged"] == True) &
                (mode_df["actual_failure"] == True)
            ).sum()
        )

        fp = int(
            (
                (mode_df["flagged"] == True) &
                (mode_df["actual_failure"] == False)
            ).sum()
        )

        fn = int(
            (
                (mode_df["flagged"] == False) &
                (mode_df["actual_failure"] == True)
            ).sum()
        )

        tn = int(
            (
                (mode_df["flagged"] == False) &
                (mode_df["actual_failure"] == False)
            ).sum()
        )

        # -----------------------------
        # Actual RAG Failure
        # -----------------------------

        actual_failures = tp + fn

        failure_rate = (
            actual_failures / total_tests * 100
            if total_tests > 0
            else 0
        )

        # -----------------------------
        # Detector Flagged
        # -----------------------------

        detected_failures = tp + fp

        detected_rate = (
            detected_failures / total_tests * 100
            if total_tests > 0
            else 0
        )

        # -----------------------------
        # Precision
        # -----------------------------

        precision = (
            tp / (tp + fp) * 100
            if (tp + fp) > 0
            else None
        )

        # -----------------------------
        # Recall / Detection Rate
        # -----------------------------

        recall = (
            tp / (tp + fn) * 100
            if (tp + fn) > 0
            else None
        )

        # -----------------------------
        # False Positive Rate
        # -----------------------------

        false_positive_rate = (
            fp / (fp + tn) * 100
            if (fp + tn) > 0
            else None
        )

        # -----------------------------
        # False Negative Rate
        # -----------------------------

        false_negative_rate = (
            fn / (fn + tp) * 100
            if (fn + tp) > 0
            else None
        )

        # -----------------------------
        # Specificity
        # -----------------------------

        specificity = (
            tn / (tn + fp) * 100
            if (tn + fp) > 0
            else None
        )

        # -----------------------------
        # Accuracy
        # -----------------------------

        accuracy = (
            (tp + tn) / total_tests * 100
            if total_tests > 0
            else 0
        )

        summary[mode] = {

            "total_tests": total_tests,

            # RAG failures
            "actual_failures": actual_failures,
            "failure_rate_percent": round(
                failure_rate, 2
            ),

            # Detector results
            "detected_failures": detected_failures,
            "detected_rate_percent": round(
                detected_rate, 2
            ),

            # Confusion matrix
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,

            # Metrics
            "precision_percent": (
                round(precision, 2)
                if precision is not None
                else None
            ),

            "recall_percent": (
                round(recall, 2)
                if recall is not None
                else None
            ),

            "false_positive_rate_percent": (
                round(false_positive_rate, 2)
                if false_positive_rate is not None
                else None
            ),

            "false_negative_rate_percent": (
                round(false_negative_rate, 2)
                if false_negative_rate is not None
                else None
            ),

            "specificity_percent": (
                round(specificity, 2)
                if specificity is not None
                else None
            ),

            "accuracy_percent": round(
                accuracy, 2
            )
        }

    # =================================
    # OVERALL
    # =================================

    total_tests = len(df)

    tp = int(
        (
            (df["flagged"] == True) &
            (df["actual_failure"] == True)
        ).sum()
    )

    fp = int(
        (
            (df["flagged"] == True) &
            (df["actual_failure"] == False)
        ).sum()
    )

    fn = int(
        (
            (df["flagged"] == False) &
            (df["actual_failure"] == True)
        ).sum()
    )

    tn = int(
        (
            (df["flagged"] == False) &
            (df["actual_failure"] == False)
        ).sum()
    )

    actual_failures = tp + fn
    detected_failures = tp + fp

    failure_rate = (
        actual_failures / total_tests * 100
        if total_tests > 0
        else 0
    )

    detected_rate = (
        detected_failures / total_tests * 100
        if total_tests > 0
        else 0
    )

    precision = (
        tp / (tp + fp) * 100
        if (tp + fp) > 0
        else None
    )

    recall = (
        tp / (tp + fn) * 100
        if (tp + fn) > 0
        else None
    )

    false_positive_rate = (
        fp / (fp + tn) * 100
        if (fp + tn) > 0
        else None
    )

    false_negative_rate = (
        fn / (fn + tp) * 100
        if (fn + tp) > 0
        else None
    )

    specificity = (
        tn / (tn + fp) * 100
        if (tn + fp) > 0
        else None
    )

    accuracy = (
        (tp + tn) / total_tests * 100
        if total_tests > 0
        else 0
    )

    summary["overall"] = {

        "total_tests": total_tests,

        "actual_failures": actual_failures,
        "failure_rate_percent": round(
            failure_rate, 2
        ),

        "detected_failures": detected_failures,
        "detected_rate_percent": round(
            detected_rate, 2
        ),

        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,

        "precision_percent": (
            round(precision, 2)
            if precision is not None
            else None
        ),

        "recall_percent": (
            round(recall, 2)
            if recall is not None
            else None
        ),

        "false_positive_rate_percent": (
            round(false_positive_rate, 2)
            if false_positive_rate is not None
            else None
        ),

        "false_negative_rate_percent": (
            round(false_negative_rate, 2)
            if false_negative_rate is not None
            else None
        ),

        "specificity_percent": (
            round(specificity, 2)
            if specificity is not None
            else None
        ),

        "accuracy_percent": round(
            accuracy, 2
        )
    }

    # =================================
    # SAVE JSON
    # =================================

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            summary,
            f,
            indent=4
        )

    # =================================
    # PRINT REPORT
    # =================================

    print("\n========================================")
    print("       RED TEAM EVALUATION SUMMARY")
    print("========================================\n")

    for mode, values in summary.items():

        print(f"--- {mode.upper()} ---")

        print(
            f"Tests              : "
            f"{values['total_tests']}"
        )

        print(
            f"Actual failures    : "
            f"{values['actual_failures']}"
        )

        print(
            f"Failure rate       : "
            f"{values['failure_rate_percent']}%"
        )

        print(
            f"Detector flagged   : "
            f"{values['detected_failures']}"
        )

        print(
            f"Detector flag rate : "
            f"{values['detected_rate_percent']}%"
        )

        print("\nConfusion Matrix")

        print(
            f"True Positives     : "
            f"{values['true_positives']}"
        )

        print(
            f"False Positives    : "
            f"{values['false_positives']}"
        )

        print(
            f"False Negatives    : "
            f"{values['false_negatives']}"
        )

        print(
            f"True Negatives     : "
            f"{values['true_negatives']}"
        )

        print("\nDetector Metrics")

        print(
            f"Precision          : "
            f"{values['precision_percent']}%"
        )

        print(
            f"Recall             : "
            f"{values['recall_percent']}%"
        )

        print(
            f"False Positive Rate: "
            f"{values['false_positive_rate_percent']}%"
        )

        print(
            f"False Negative Rate: "
            f"{values['false_negative_rate_percent']}%"
        )

        print(
            f"Specificity        : "
            f"{values['specificity_percent']}%"
        )

        print(
            f"Accuracy           : "
            f"{values['accuracy_percent']}%"
        )

        print()

    print(
        f"Saved to: {json_path}"
    )

    return summary