import pandas as pd

input_file = "data/selected_reviews.csv"
output_file = "data/prepared_reviews.csv"

df = pd.read_csv(input_file, engine="python", on_bad_lines="skip")

df["title"] = df["title"].fillna("")
df["review"] = df["review"].fillna("")

df["full_text"] = df["title"] + " " + df["review"]

df["full_text"] = df["full_text"].str.strip()

df = df[df["full_text"] != ""]

df.to_csv(output_file, index=False)

print("Text preparation completed.")
print(df[["reviewID", "title", "review", "full_text"]].head())
