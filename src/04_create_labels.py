import sys
from pathlib import Path

# Add project root to Python path so config.py can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd

from config import PROCESSED_REVIEWS_FILE, LABELED_REVIEWS_FILE
from src.sentiment_model import SentimentLabeler


def main():
    df = pd.read_csv(PROCESSED_REVIEWS_FILE, engine="python", on_bad_lines="skip")

    labeler = SentimentLabeler()

    df["weak_rating_label"] = df["rating"].apply(labeler.create_rating_label)

    # Fast batch prediction instead of row-by-row prediction
    predictions = labeler.predict_batch(df["clean_text"].tolist())

    df[
        [
            "predicted_label",
            "sentiment_score",
            "transformer_confidence",
            "confidence",
            "sarcasm_or_context_risk",
            "mixed_sentiment_flag",
        ]
    ] = pd.DataFrame(predictions, index=df.index)

    df["rating_prediction_conflict"] = df["weak_rating_label"] != df["predicted_label"]

    df["needs_human_review"] = (
        df["rating_prediction_conflict"]
        | (df["confidence"] == "low")
        | (df["predicted_label"] == "uncertain")
        | df["sarcasm_or_context_risk"]
        | df["mixed_sentiment_flag"]
    )

    df.to_csv(LABELED_REVIEWS_FILE, index=False)

    print("Labels created successfully.")
    print(f"Input file: {PROCESSED_REVIEWS_FILE}")
    print(f"Output file: {LABELED_REVIEWS_FILE}")
    print(
        df[
            [
                "rating",
                "clean_text",
                "weak_rating_label",
                "predicted_label",
                "sentiment_score",
                "transformer_confidence",
                "confidence",
                "rating_prediction_conflict",
                "sarcasm_or_context_risk",
                "mixed_sentiment_flag",
                "needs_human_review",
            ]
        ].head()
    )


if __name__ == "__main__":
    main()
