import pandas as pd

input_file = "data/final_reviews_with_language_flags.csv"
uncertain_input_file = "data/uncertain_reviews.csv"

final_output_file = "data/portfolio_final_reviews.csv"
mismatch_output_file = "data/portfolio_mismatch_report.csv"
summary_output_file = "data/portfolio_summary_report.csv"

df = pd.read_csv(input_file)

# Ensure required columns exist
if "rating_prediction_agreement" not in df.columns:
    df["rating_prediction_agreement"] = df["weak_rating_label"] == df["predicted_label"]

if "rating_prediction_conflict" not in df.columns:
    df["rating_prediction_conflict"] = df["weak_rating_label"] != df["predicted_label"]

# Load uncertain predictions if available
try:
    uncertain_df = pd.read_csv(uncertain_input_file)
    uncertain_count = len(uncertain_df)
except FileNotFoundError:
    uncertain_count = 0

# Save full final dataset
df.to_csv(final_output_file, index=False)

# Save mismatch/conflict report
mismatches = df[df["rating_prediction_agreement"] == False].copy()
mismatches.to_csv(mismatch_output_file, index=False)

# Summary numbers
total_reviews = len(df)
matched_reviews = df["rating_prediction_agreement"].sum()
mismatched_reviews = total_reviews - matched_reviews

match_percentage = (matched_reviews / total_reviews) * 100 if total_reviews > 0 else 0
mismatch_percentage = (
    (mismatched_reviews / total_reviews) * 100 if total_reviews > 0 else 0
)

weak_label_counts = df["weak_rating_label"].value_counts()
predicted_label_counts = df["predicted_label"].value_counts()
language_flag_counts = df["language_flag"].value_counts()

confidence_counts = (
    df["confidence"].value_counts()
    if "confidence" in df.columns
    else pd.Series(dtype=int)
)

summary_data = {
    "metric": [
        "total_reviews_after_removing_uncertain",
        "uncertain_reviews_removed",
        "matched_reviews",
        "mismatched_reviews",
        "match_percentage",
        "mismatch_percentage",
        "weak_positive_count",
        "weak_neutral_count",
        "weak_negative_count",
        "predicted_positive_count",
        "predicted_neutral_count",
        "predicted_negative_count",
        "english_count",
        "unknown_count",
        "non_english_count",
        "high_confidence_count",
        "medium_confidence_count",
        "low_confidence_count",
    ],
    "value": [
        total_reviews,
        uncertain_count,
        matched_reviews,
        mismatched_reviews,
        round(match_percentage, 2),
        round(mismatch_percentage, 2),
        weak_label_counts.get("positive", 0),
        weak_label_counts.get("neutral", 0),
        weak_label_counts.get("negative", 0),
        predicted_label_counts.get("positive", 0),
        predicted_label_counts.get("neutral", 0),
        predicted_label_counts.get("negative", 0),
        language_flag_counts.get("english", 0),
        language_flag_counts.get("unknown", 0),
        language_flag_counts.get("non_english", 0),
        confidence_counts.get("high", 0),
        confidence_counts.get("medium", 0),
        confidence_counts.get("low", 0),
    ],
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(summary_output_file, index=False)

print("Reports exported successfully.")
print("--------------------------------")
print(f"Final dataset: {final_output_file}")
print(f"Mismatch report: {mismatch_output_file}")
print(f"Summary report: {summary_output_file}")

print("\nSummary:")
print(summary_df)
