import pandas as pd
from langdetect import detect, DetectorFactory, LangDetectException

"""
Language detection follows:
docs/annotation_guidelines.md

Important:
Non-English text is not automatically wrong.

Meaning:
- English text can continue normally.
- Non-English text should be flagged for multilingual or human review.
- Unknown language should also be flagged for review.

This keeps the project aligned with the annotation guideline:
If non-English meaning is understood, it can still be labeled normally.
If unclear, it should be reviewed.
"""

# Ensure consistent language detection results
DetectorFactory.seed = 0

input_file = "data/final_reviews.csv"
output_file = "data/final_reviews_with_language_flags.csv"

df = pd.read_csv(input_file)


def detect_language(text):
    """
    Detect language from clean text.

    Returns:
    - language code such as 'en', 'es', 'fr'
    - 'unknown' if text is too short or detection fails
    """
    text = str(text).strip()

    if len(text) < 5:
        return "unknown"

    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "unknown"


def create_language_flag(lang):
    """
    Convert detected language into simple project labels.

    english      = detected English text
    non_english  = detected language other than English
    unknown      = language could not be detected
    """
    if lang == "en":
        return "english"
    elif lang == "unknown":
        return "unknown"
    else:
        return "non_english"


def create_language_review_reason(row):
    """
    Create a clear reason for language review.

    Non-English is not treated as an automatic mistake.
    It is treated as a review signal.
    """
    language_flag = row["language_flag"]
    detected_language = row["detected_language"]

    if language_flag == "english":
        return "no_language_review_needed"

    if language_flag == "unknown":
        return "unknown_language_or_too_short_text"

    return f"non_english_text_detected_{detected_language}"


# Detect language
df["detected_language"] = df["clean_text"].apply(detect_language)

# Create language flag
df["language_flag"] = df["detected_language"].apply(create_language_flag)

# Create review flag
# True means the row may need human or multilingual review
df["needs_language_review"] = df["language_flag"].isin(["non_english", "unknown"])

# Create review reason
df["language_review_reason"] = df.apply(create_language_review_reason, axis=1)

# Save
df.to_csv(output_file, index=False)

print("Language detection completed (langdetect).")
print(f"Output file: {output_file}")

print(
    df[
        [
            "clean_text",
            "detected_language",
            "language_flag",
            "needs_language_review",
            "language_review_reason",
        ]
    ].head()
)
