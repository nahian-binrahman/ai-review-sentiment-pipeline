import pandas as pd
import re
import html

input_file = "data/prepared_reviews.csv"
output_file = "data/processed_reviews.csv"

def clean_text(text):
    text = str(text)

    # Convert HTML entities and remove HTML tags like <br>
    text = html.unescape(text)
    text = re.sub(r"<.*?>", " ", text)

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove special characters but keep letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

df = pd.read_csv(input_file)

df["clean_text"] = df["full_text"].apply(clean_text)

df = df[df["clean_text"].str.len() > 5]

df.to_csv(output_file, index=False)

print("Text cleaning completed.")
print(df[["reviewID", "full_text", "clean_text"]].head())