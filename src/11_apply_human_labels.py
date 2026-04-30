import pandas as pd

# Input files
human_review_file = "data/human_review_queue.csv"
final_file = "data/final_reviews.csv"
uncertain_file = "data/uncertain_reviews.csv"

# Output file
output_file = "data/final_approved_reviews.csv"


# Load human review queue
review_df = pd.read_csv(human_review_file)

# Load final evaluated reviews
final_df = pd.read_csv(final_file)

# Load uncertain reviews if available
try:
    uncertain_df = pd.read_csv(uncertain_file)
except FileNotFoundError:
    uncertain_df = pd.DataFrame()


# Combine evaluated reviews + uncertain reviews
combined_df = pd.concat([final_df, uncertain_df], ignore_index=True)

# Remove duplicate review IDs if reviewID exists
if "reviewID" in combined_df.columns:
    combined_df = combined_df.drop_duplicates(subset=["reviewID"])


# --------------------------------------------------
# Final label logic
# --------------------------------------------------
# weak_rating_label = rating-based weak reference label
# predicted_label = AI-generated label
# human_label = trusted label if reviewed
# final_label = best available final label
#
# Rule:
# 1. Start with AI predicted label
# 2. If human reviewed the row and gave a valid label,
#    replace AI label with human label
# --------------------------------------------------

combined_df["final_label"] = combined_df["predicted_label"]

# Keep only rows that were actually reviewed by a human
reviewed_df = review_df[review_df["review_status"] == "reviewed"].copy()

# Valid sentiment labels
valid_labels = ["positive", "neutral", "negative"]

# Apply human labels
for _, row in reviewed_df.iterrows():
    review_id = row["reviewID"]
    human_label = str(row["human_label"]).strip().lower()

    if human_label in valid_labels:
        combined_df.loc[combined_df["reviewID"] == review_id, "final_label"] = (
            human_label
        )


# Optional: add label source column
def get_label_source(row):
    review_id = row["reviewID"]

    matched_review = reviewed_df[reviewed_df["reviewID"] == review_id]

    if not matched_review.empty:
        human_label = str(matched_review.iloc[0]["human_label"]).strip().lower()

        if human_label in valid_labels:
            return "human_reviewed"

    return "ai_predicted"


combined_df["final_label_source"] = combined_df.apply(get_label_source, axis=1)


# Save final approved dataset
combined_df.to_csv(output_file, index=False)


print("Final approved labels created successfully.")
print("-----------------------------------------")
print(f"Reviewed rows found: {len(reviewed_df)}")
print(f"Total final approved rows: {len(combined_df)}")
print(f"Output file: {output_file}")

print()
print("Final label source counts:")
print(combined_df["final_label_source"].value_counts())
