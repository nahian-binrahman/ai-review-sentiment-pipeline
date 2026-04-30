import pandas as pd

input_file = "data/final_reviews.csv"
output_file = "data/rating_prediction_conflicts.csv"

df = pd.read_csv(input_file)

# -----------------------------
# Step 1: Ensure conflict column exists
# -----------------------------
# If you already created it in previous steps, this is safe
if "rating_prediction_conflict" not in df.columns:
    df["rating_prediction_conflict"] = df["weak_rating_label"] != df["predicted_label"]

# -----------------------------
# Step 2: Select only conflict rows
# -----------------------------
conflicts = df[df["rating_prediction_conflict"] == True].copy()

# -----------------------------
# Step 3: Select important columns for analysis
# -----------------------------
conflict_report = conflicts[
    [
        "reviewID",
        "rating",
        "weak_rating_label",
        "predicted_label",
        "confidence",
        "title",
        "review",
        "clean_text",
        "verifiedPurchase",
    ]
]

# -----------------------------
# Step 4: Save report
# -----------------------------
conflict_report.to_csv(output_file, index=False)

# -----------------------------
# Step 5: Print summary
# -----------------------------
print("Rating vs Prediction Conflict Analysis Completed")
print("------------------------------------------------")
print(f"Total conflicts found: {len(conflict_report)}")
print(f"Output file: {output_file}")

print("\nFirst few conflict examples:")
print(
    conflict_report[
        ["reviewID", "rating", "weak_rating_label", "predicted_label", "clean_text"]
    ].head()
)
