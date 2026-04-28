import pandas as pd

input_file = "data/mismatched_reviews.csv"
output_file = "data/mistake_analysis_report.csv"

df = pd.read_csv(input_file)

spanish_words = [
    "excelente",
    "excelentes",
    "esposo",
    "encantan",
    "muy",
    "bueno",
    "buenos",
    "producto",
    "gracias"
]

def find_mistake_reason(text):
    text = str(text).lower()

    if any(word in text for word in spanish_words):
        return "non_english_text"

    if len(text.split()) <= 3:
        return "short_text"

    return "needs_manual_review"

df["mistake_reason"] = df["clean_text"].apply(find_mistake_reason)

df.to_csv(output_file, index=False)

print("Mistake reasons added successfully.")
print(f"Output file: {output_file}")

print(df[["clean_text", "rating_label", "predicted_label", "mistake_reason"]].head())