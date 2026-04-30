import subprocess
import sys
import time
import os
from pathlib import Path

"""
Run the complete AI data labeling pipeline.

This script runs all src pipeline files in the correct order.

Usage:
    python run_pipeline.py
"""

PROJECT_ROOT = Path(__file__).resolve().parent

# Ensure required folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("assets", exist_ok=True)

PIPELINE_STEPS = [
    "src/01_load_and_select.py",
    "src/02_prepare_text.py",
    "src/03_clean_text.py",
    "src/04_create_labels.py",
    "src/05_compare_labels.py",
    "src/06_analyze_conflicts.py",
    "src/07_detect_language_issues.py",
    "src/06b_add_mistake_reasons.py",
    "src/07b_create_english_only_dataset.py",
    "src/08_export_reports.py",
    "src/09_create_charts.py",
    "src/10_create_human_review_file.py",
    "src/11_apply_human_labels.py",
]


def run_step(step_path):
    """
    Run one pipeline step.
    If a step fails, stop pipeline safely.
    """
    full_path = PROJECT_ROOT / step_path

    print("\n" + "=" * 70)
    print(f"Running: {step_path}")
    print("=" * 70)

    try:
        if not full_path.exists():
            raise FileNotFoundError(f"Missing pipeline file: {step_path}")

        start_time = time.time()

        result = subprocess.run(
            [sys.executable, str(full_path)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
        )

        # Print output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        # Check for failure
        if result.returncode != 0:
            raise RuntimeError(f"Step failed: {step_path}")

        end_time = time.time()
        print(f"Finished {step_path} in {round(end_time - start_time, 2)} seconds")

        return True

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print(f"Step: {step_path}")
        print(f"Error: {str(e)}")
        print("Pipeline stopped.")
        return False


def main():
    print("Starting AI Data Labeling Pipeline")
    print("----------------------------------")

    for step in PIPELINE_STEPS:
        success = run_step(step)

        if not success:
            break

    else:
        print("\n" + "=" * 70)
        print("Pipeline completed successfully!")
        print("=" * 70)


if __name__ == "__main__":
    main()
