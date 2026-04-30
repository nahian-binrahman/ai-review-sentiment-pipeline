import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)

input_file = "data/portfolio_final_reviews.csv"
df = pd.read_csv(input_file)

# --------------------------------------------------
# Ensure required columns exist
# --------------------------------------------------
if "rating_prediction_agreement" not in df.columns:
    df["rating_prediction_agreement"] = df["weak_rating_label"] == df["predicted_label"]

# --------------------------------------------------
# Chart 1: Weak Rating Label Distribution
# --------------------------------------------------
plt.figure()
df["weak_rating_label"].value_counts().plot(kind="bar")
plt.title("Weak Rating Label Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/weak_rating_label_distribution.png")
plt.close()

# --------------------------------------------------
# Chart 2: Predicted Label Distribution
# --------------------------------------------------
plt.figure()
df["predicted_label"].value_counts().plot(kind="bar")
plt.title("Predicted Label Distribution")
plt.xlabel("Label")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/predicted_label_distribution.png")
plt.close()

# --------------------------------------------------
# Chart 3: Agreement vs Conflict
# --------------------------------------------------
plt.figure()
df["rating_prediction_agreement"].value_counts().plot(kind="bar")
plt.title("Agreement vs Conflict")
plt.xlabel("Agreement (True = Match)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("assets/agreement_vs_conflict.png")
plt.close()

print("Charts created successfully!")
