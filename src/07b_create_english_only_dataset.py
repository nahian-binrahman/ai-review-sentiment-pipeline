import pandas as pd

input_file = "data/final_reviews_with_language_flags.csv"
output_file = "data/english_only_reviews.csv"

df = pd.read_csv(input_file)

english_df = df[df["language_flag"] == "english_or_unknown"]

english_df.to_csv(output_file, index=False)

print("English-only dataset created.")
print(f"Total original rows: {len(df)}")
print(f"English-only rows: {len(english_df)}")
print(f"Output file: {output_file}")