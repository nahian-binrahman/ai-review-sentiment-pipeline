import pandas as pd

final_reviews_file = "data/final_reviews.csv"
uncertain_reviews_file = "data/uncertain_reviews.csv"
output_file = "data/human_review_queue.csv"

# Load final evaluated rows
final_df = pd.read_csv(final_reviews_file)

# --------------------------------------------------
# STEP 1: Ensure conflict column exists
# --------------------------------------------------
# If you followed Step 2 earlier, this column already exists
# Otherwise, create it here

if "rating_prediction_conflict" not in final_df.columns:
    final_df["rating_prediction_conflict"] = (
        final_df["weak_rating_label"] != final_df["predicted_label"]
    )

# --------------------------------------------------
# STEP 2: Select rows needing review
# --------------------------------------------------
# Conditions:
# - rating vs prediction conflict
# - OR low confidence

if "confidence" in final_df.columns:
    review_df = final_df[
        (final_df["rating_prediction_conflict"] == True)
        | (final_df["confidence"] == "low")
    ].copy()
else:
    review_df = final_df[final_df["rating_prediction_conflict"] == True].copy()

# --------------------------------------------------
# STEP 3: Load uncertain predictions
# --------------------------------------------------
try:
    uncertain_df = pd.read_csv(uncertain_reviews_file)

    # Add missing columns if needed
    if "rating_prediction_conflict" not in uncertain_df.columns:
        uncertain_df["rating_prediction_conflict"] = False

    # Add reason column
    uncertain_df["review_reason"] = "uncertain_prediction"

except FileNotFoundError:
    uncertain_df = pd.DataFrame()

# --------------------------------------------------
# STEP 4: Assign review reasons (UPDATED LOGIC)
# --------------------------------------------------
if not review_df.empty:
    review_df["review_reason"] = review_df.apply(
        lambda row: (
            "rating_prediction_conflict_and_low_confidence"
            if row.get("rating_prediction_conflict") == True
            and row.get("confidence") == "low"
            else (
                "rating_prediction_conflict"
                if row.get("rating_prediction_conflict") == True
                else "low_confidence"
            )
        ),
        axis=1,
    )

# --------------------------------------------------
# STEP 5: Combine all review cases
# --------------------------------------------------
human_review_df = pd.concat([review_df, uncertain_df], ignore_index=True)

# --------------------------------------------------
# STEP 6: Remove duplicates
# --------------------------------------------------
if "reviewID" in human_review_df.columns:
    human_review_df = human_review_df.drop_duplicates(subset=["reviewID"])

# --------------------------------------------------
# STEP 7: Add human annotation columns
# --------------------------------------------------
human_review_df["human_label"] = ""
human_review_df["review_status"] = "needs_review"
human_review_df["review_notes"] = ""

# --------------------------------------------------
# STEP 8: Save output
# --------------------------------------------------
human_review_df.to_csv(output_file, index=False)

print("Human review queue created successfully.")
print(f"Rows needing review: {len(human_review_df)}")
print(f"Output file: {output_file}")

# --------------------------------------------------
# STEP 9: Summary of reasons
# --------------------------------------------------
if "review_reason" in human_review_df.columns:
    print("\nReview reason counts:")
    print(human_review_df["review_reason"].value_counts())
