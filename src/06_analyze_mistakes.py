import pandas as pd

input_file = "data/final_reviews.csv"
output_file = "data/mismatched_reviews.csv"

df = pd.read_csv(input_file)

# Select only mismatched rows
mismatches = df[df["label_match"] == False]

# Select important columns for review
mismatch_report = mismatches[
    [
        "reviewID",
        "rating",
        "title",
        "review",
        "clean_text",
        "rating_label",
        "predicted_label",
        "verifiedPurchase"
    ]
]

# Save mismatch report
mismatch_report.to_csv(output_file, index=False)

print("Mistake analysis completed.")
print("---------------------------")
print(f"Total mismatches found: {len(mismatch_report)}")
print(f"Output file: {output_file}")

print("\nFirst few mismatched examples:")
print(
    mismatch_report[
        ["reviewID", "rating", "clean_text", "rating_label", "predicted_label"]
    ].head()
)