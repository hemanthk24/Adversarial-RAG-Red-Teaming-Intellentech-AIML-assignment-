from evaluation.eval import generate_failure_summary
import pandas as pd

if __name__ == "__main__":
    # Load the test results from the CSV file
    path_base= "results/baseline_red_team_test_results_summary.csv"
    
    updated_path = "results/after_update_red_team_test_results_summary.csv"

    # Generate the failure summary
    summary = generate_failure_summary(csv_path=updated_path)