import pandas as pd

input_file = "data/final_reviews_with_language_flags.csv"
output_file = "data/conflict_analysis_report.csv"

df = pd.read_csv(input_file)

# Keep only rows where weak rating label and model prediction disagree.
# These are conflicts, not confirmed mistakes.
df = df[df["rating_prediction_conflict"] == True].copy()


positive_words = [
    "good",
    "great",
    "excellent",
    "amazing",
    "perfect",
    "love",
    "loved",
    "nice",
    "best",
    "happy",
    "recommend",
]

negative_words = [
    "bad",
    "poor",
    "terrible",
    "awful",
    "broken",
    "broke",
    "waste",
    "hate",
    "disappointed",
    "worst",
    "cheap",
    "return",
    "refund",
]


def find_review_reason(row):
    """
    Find why a row needs review.

    Important:
    This file does not assume the model is wrong.

    A conflict means:
    - weak_rating_label and predicted_label disagree
    - the row should be reviewed
    - the final decision may need human judgment

    Non-English text is not treated as an automatic mistake.
    It is treated as a multilingual review signal.
    """
    text = str(row["clean_text"]).lower()
    words = text.split()

    weak_rating_label = row["weak_rating_label"]
    predicted_label = row["predicted_label"]

    language_flag = row.get("language_flag", "unknown")
    detected_language = row.get("detected_language", "unknown")
    needs_language_review = row.get("needs_language_review", False)

    # 1. Non-English text
    # Not a mistake, but should be reviewed by someone who understands the language.
    if language_flag == "non_english":
        return f"needs_multilingual_review_{detected_language}"

    # 2. Unknown language / too short / unclear language
    if language_flag == "unknown" or needs_language_review == True:
        return "needs_language_review_unknown_or_too_short"

    # 3. Very short text
    if len(words) <= 3:
        return "short_or_low_context_text"

    # 4. Mixed sentiment
    if "but" in words or "however" in words or "although" in words:
        return "mixed_sentiment_needs_review"

    # 5. Possible sarcasm or context conflict
    if any(pos in text for pos in positive_words) and any(
        neg in text for neg in negative_words
    ):
        return "possible_sarcasm_or_context_conflict"

    # 6. Rating weak label says positive, model says neutral/negative
    if weak_rating_label == "positive" and predicted_label in ["neutral", "negative"]:
        return "rating_positive_but_text_prediction_lower"

    # 7. Rating weak label says negative, model says neutral/positive
    if weak_rating_label == "negative" and predicted_label in ["neutral", "positive"]:
        return "rating_negative_but_text_prediction_higher"

    # 8. Rating weak label says neutral, model says positive/negative
    if weak_rating_label == "neutral" and predicted_label in ["positive", "negative"]:
        return "rating_neutral_but_text_has_sentiment"

    # 9. General fallback
    return "needs_manual_review"


df["review_reason"] = df.apply(find_review_reason, axis=1)

df.to_csv(output_file, index=False)

print("Conflict analysis report created successfully.")
print(f"Total conflicts analyzed: {len(df)}")
print(f"Output file: {output_file}")

print(
    df[
        [
            "clean_text",
            "weak_rating_label",
            "predicted_label",
            "detected_language",
            "language_flag",
            "needs_language_review",
            "review_reason",
        ]
    ].head()
)
