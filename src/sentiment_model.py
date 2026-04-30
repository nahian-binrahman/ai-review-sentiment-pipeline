from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

from config import (
    TRANSFORMER_MODEL_NAME,
    TRANSFORMER_BATCH_SIZE,
    SHORT_TEXT_WORD_LIMIT,
    LOW_CONFIDENCE_THRESHOLD,
    HIGH_CONFIDENCE_THRESHOLD,
    MEDIUM_CONFIDENCE_THRESHOLD,
    RULE_STRENGTH_THRESHOLD,
)


class SentimentLabeler:
    def __init__(self):
        print("Loading VADER analyzer...")
        self.vader_analyzer = SentimentIntensityAnalyzer()

        print("Loading Transformer sentiment model...")
        self.transformer_sentiment = pipeline(
            "sentiment-analysis",
            model=TRANSFORMER_MODEL_NAME,
        )
        print("Transformer model loaded successfully.")

    def create_rating_label(self, rating):
        if rating >= 4:
            return "positive"
        elif rating <= 2:
            return "negative"
        else:
            return "neutral"

    def get_textblob_score(self, text):
        return TextBlob(str(text)).sentiment.polarity

    def get_vader_score(self, text):
        return self.vader_analyzer.polarity_scores(str(text))["compound"]

    def normalize_transformer_label(self, label):
        label = str(label).lower()

        label_map = {
            "label_0": "negative",
            "label_1": "neutral",
            "label_2": "positive",
        }

        return label_map.get(label, label)

    def create_confidence_level(self, transformer_confidence, rule_score):
        rule_strength = abs(rule_score)

        if (
            transformer_confidence >= HIGH_CONFIDENCE_THRESHOLD
            and rule_strength >= RULE_STRENGTH_THRESHOLD
        ):
            return "high"
        elif transformer_confidence >= MEDIUM_CONFIDENCE_THRESHOLD:
            return "medium"
        else:
            return "low"

    def detect_sarcasm_or_context_risk(self, text):
        text = str(text).lower()

        positive_words = [
            "great",
            "amazing",
            "excellent",
            "perfect",
            "love",
            "nice",
            "good",
        ]

        negative_context_words = [
            "broke",
            "broken",
            "stopped working",
            "waste",
            "refund",
            "return",
            "terrible",
            "awful",
            "disappointed",
            "worst",
        ]

        has_positive_word = any(word in text for word in positive_words)
        has_negative_context = any(word in text for word in negative_context_words)

        return has_positive_word and has_negative_context

    def detect_mixed_sentiment(self, text):
        text = str(text).lower()
        words = text.split()

        return any(word in words for word in ["but", "however", "although"])

    def predict_batch(self, texts):
        """
        Faster batch prediction.

        Returns one tuple per text:
        predicted_label,
        sentiment_score,
        transformer_confidence,
        confidence,
        sarcasm_or_context_risk,
        mixed_sentiment_flag
        """

        texts = [str(text).lower().strip() for text in texts]

        results = [None] * len(texts)

        valid_indices = []
        valid_texts = []

        for index, text in enumerate(texts):
            if text == "":
                results[index] = ("uncertain", 0.0, 0.0, "low", True, False)

            elif len(text.split()) <= SHORT_TEXT_WORD_LIMIT:
                results[index] = ("uncertain", 0.0, 0.0, "low", True, False)

            else:
                valid_indices.append(index)
                valid_texts.append(text[:512])

        if valid_texts:
            transformer_outputs = self.transformer_sentiment(
                valid_texts,
                batch_size=TRANSFORMER_BATCH_SIZE,
                truncation=True,
            )

            for index, transformer_output in zip(valid_indices, transformer_outputs):
                text = texts[index]

                textblob_score = self.get_textblob_score(text)
                vader_score = self.get_vader_score(text)
                rule_score = (textblob_score + vader_score) / 2

                transformer_label = self.normalize_transformer_label(
                    transformer_output["label"]
                )
                transformer_confidence = transformer_output["score"]

                sarcasm_or_context_risk = self.detect_sarcasm_or_context_risk(text)
                mixed_sentiment_flag = self.detect_mixed_sentiment(text)

                if transformer_confidence < LOW_CONFIDENCE_THRESHOLD:
                    predicted_label = "uncertain"
                    confidence = "low"
                else:
                    predicted_label = transformer_label
                    confidence = self.create_confidence_level(
                        transformer_confidence,
                        rule_score,
                    )

                results[index] = (
                    predicted_label,
                    rule_score,
                    transformer_confidence,
                    confidence,
                    sarcasm_or_context_risk,
                    mixed_sentiment_flag,
                )

        return results
