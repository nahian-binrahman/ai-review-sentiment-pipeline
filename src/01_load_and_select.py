import pandas as pd

input_file = "data/raw_reviews.csv"
output_file = "data/selected_reviews.csv"

df = pd.read_csv(input_file, engine="python", on_bad_lines="skip")

useful_columns = [
    "reviewID",
    "date",
    "verifiedPurchase",
    "rating",
    "helpful",
    "title",
    "review",
    "country",
    "helpful_aug",
    "helpfulness_score",
]

df = df[useful_columns]

df.to_csv(output_file, index=False)

print("Selected columns saved successfully.")
print(df.head())
