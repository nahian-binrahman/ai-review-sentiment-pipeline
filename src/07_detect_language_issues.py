import pandas as pd

input_file = "data/final_reviews.csv"
output_file = "data/final_reviews_with_language_flags.csv"

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
    "gracias",
    "para",
    "con",
    "calidad"
]

def detect_language_issue(text):
    text = str(text).lower()

    for word in spanish_words:
        if word in text:
            return "possible_non_english"

    return "english_or_unknown"

df["language_flag"] = df["clean_text"].apply(detect_language_issue)

df.to_csv(output_file, index=False)

print("Language issue detection completed.")
print(f"Output file: {output_file}")

print(df[["reviewID", "clean_text", "language_flag"]].head())