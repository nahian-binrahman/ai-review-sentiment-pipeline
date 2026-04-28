import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/portfolio_final_reviews.csv")

# Chart 1: Label distribution
df["rating_label"].value_counts().plot(kind="bar")
plt.title("Rating Label Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/label_distribution.png")
plt.clf()

# Chart 2: Match vs Mismatch
df["label_match"].value_counts().plot(kind="bar")
plt.title("Prediction Accuracy")
plt.xlabel("Match")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/match_vs_mismatch.png")