import pandas as pd

input_file = "data/labeled_reviews.csv"
output_file = "data/final_reviews.csv"

df = pd.read_csv(input_file)

# Compare rating label and AI predicted label
df["label_match"] = df["rating_label"] == df["predicted_label"]

# Count total reviews
total_reviews = len(df)

# Count matched and mismatched labels
matched_reviews = df["label_match"].sum()
mismatched_reviews = total_reviews - matched_reviews

# Calculate percentage
match_percentage = (matched_reviews / total_reviews) * 100
mismatch_percentage = (mismatched_reviews / total_reviews) * 100

print("Label Comparison Result")
print("-----------------------")
print(f"Total reviews: {total_reviews}")
print(f"Matched labels: {matched_reviews}")
print(f"Mismatched labels: {mismatched_reviews}")
print(f"Match percentage: {match_percentage:.2f}%")
print(f"Mismatch percentage: {mismatch_percentage:.2f}%")

# Save final file
df.to_csv(output_file, index=False)

print("\nFinal file saved successfully.")
print(f"Output file: {output_file}")