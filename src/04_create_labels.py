import pandas as pd
from textblob import TextBlob

input_file = "data/processed_reviews.csv"
output_file = "data/labeled_reviews.csv"


def create_rating_label(rating):
    """
    Convert star rating into sentiment label.
    4-5 = positive
    3 = neutral
    1-2 = negative
    """
    if rating >= 4:
        return "positive"
    elif rating <= 2:
        return "negative"
    else:
        return "neutral"


def create_predicted_label(text):
    """
    Use TextBlob to predict sentiment from clean text.
    """
    polarity = TextBlob(str(text)).sentiment.polarity

    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"


df = pd.read_csv(input_file)

df["rating_label"] = df["rating"].apply(create_rating_label)

df["predicted_label"] = df["clean_text"].apply(create_predicted_label)

df.to_csv(output_file, index=False)

print("Labels created successfully.")
print(df[["rating", "clean_text", "rating_label", "predicted_label"]].head())