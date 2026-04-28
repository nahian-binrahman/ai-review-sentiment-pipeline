import pandas as pd

input_file = "data/final_reviews_with_language_flags.csv"

final_output_file = "data/portfolio_final_reviews.csv"
mismatch_output_file = "data/portfolio_mismatch_report.csv"
summary_output_file = "data/portfolio_summary_report.csv"

df = pd.read_csv(input_file)

# Save full final dataset
df.to_csv(final_output_file, index=False)

# Save mismatch report
mismatches = df[df["label_match"] == False]
mismatches.to_csv(mismatch_output_file, index=False)

# Create summary numbers
total_reviews = len(df)
matched_reviews = df["label_match"].sum()
mismatched_reviews = total_reviews - matched_reviews

match_percentage = (matched_reviews / total_reviews) * 100
mismatch_percentage = (mismatched_reviews / total_reviews) * 100

rating_label_counts = df["rating_label"].value_counts()
predicted_label_counts = df["predicted_label"].value_counts()
language_flag_counts = df["language_flag"].value_counts()

summary_data = {
    "metric": [
        "total_reviews",
        "matched_reviews",
        "mismatched_reviews",
        "match_percentage",
        "mismatch_percentage",
        "rating_positive_count",
        "rating_neutral_count",
        "rating_negative_count",
        "predicted_positive_count",
        "predicted_neutral_count",
        "predicted_negative_count",
        "english_or_unknown_count",
        "possible_non_english_count"
    ],
    "value": [
        total_reviews,
        matched_reviews,
        mismatched_reviews,
        round(match_percentage, 2),
        round(mismatch_percentage, 2),
        rating_label_counts.get("positive", 0),
        rating_label_counts.get("neutral", 0),
        rating_label_counts.get("negative", 0),
        predicted_label_counts.get("positive", 0),
        predicted_label_counts.get("neutral", 0),
        predicted_label_counts.get("negative", 0),
        language_flag_counts.get("english_or_unknown", 0),
        language_flag_counts.get("possible_non_english", 0)
    ]
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