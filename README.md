<h1 align="center">🚀AI-Powered Sentiment Labeling Pipeline</h1>

<p align="center">
  <b>Human-in-the-Loop Sentiment Analysis System for Real-World AI Data Quality</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python"/>
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-purple?logo=pandas"/>
  <img src="https://img.shields.io/badge/TextBlob-NLP-green"/>
  <img src="https://img.shields.io/badge/VADER-Sentiment-orange"/>
  <img src="https://img.shields.io/badge/LangDetect-Language-yellow"/>
  <img src="https://img.shields.io/badge/Status-Advanced-brightgreen"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey"/>
</p>

---

## 🎯 Overview

This project simulates a **real-world AI data labeling pipeline** used in production systems.

Instead of focusing only on model training, it focuses on the **entire data lifecycle**:

- From raw data → cleaned data → labeled data → validated data

💡 The goal is simple:

> Build **high-quality labeled datasets**, not just models.

---

## ⚠️ Dataset Note

- Uses a **small demo dataset**
- Focus is on **workflow correctness**, not model accuracy

---

## 🔥 Key Features

- 🧹 Data preprocessing & cleaning
- 🏷️ Weak labeling from ratings
- 🤖 Hybrid sentiment prediction (TextBlob + VADER)
- ⚠️ Conflict detection (rating vs prediction)
- 🧪 Evaluation with ML metrics
- 🌍 Language detection & filtering
- 🤝 Human-in-the-loop validation
- ✅ Final high-quality dataset creation

---

## 🧠 Pipeline Overview

```text
Raw Reviews
   ↓
Clean Text
   ↓
Weak Label (Rating)
   ↓
AI Prediction
   ↓
Conflict Detection
   ↓
Evaluation
   ↓
Language Detection
   ↓
Human Review (HITL)
   ↓
Final Approved Labels
```

---

## 🧩 Problem → Solution → Outcome

### ❗ Problem

Ratings are often **noisy and unreliable**.

### 💡 Solution

Combine:

- Weak labels (ratings)
- AI predictions
- Human validation

### 🎯 Outcome

A **reliable labeled dataset** ready for real-world AI use.

---

## 🏷️ Weak Labeling Strategy

Ratings are treated as **weak signals**, not ground truth.

| Rating | Label    |
| ------ | -------- |
| 4–5 ⭐ | positive |
| 3 ⭐   | neutral  |
| 1–2 ⭐ | negative |

💡 Stored as: `weak_rating_label`

---

## 🤖 Hybrid Sentiment Model

Uses multiple signals:

- **TextBlob** → polarity
- **VADER** → rule-based scoring
- Custom logic for:
  - `but`, `however`, `although`

📌 Example:

> “Nice design, **but** it broke after 2 days”

→ Negative dominates after "but"

---

## ⚠️ Conflict Detection

Compares:

```
weak_rating_label vs predicted_label
```

If mismatch:

```
rating_prediction_conflict = True
```

These cases are flagged for review.

---

## 🧪 Uncertainty Handling

Some reviews are unclear → marked as:

```
uncertain
```

📁 Saved in:

```
data/uncertain_reviews.csv
```

Handled separately to **avoid noisy labels**.

---

## 🤝 Human-in-the-Loop (HITL)

Triggered when:

- Conflict exists
- Low confidence
- Ambiguous text

Human adds:

```
human_label
```

---

## ✅ Final Label Logic

Priority system:

```
Human > AI > Rating
```

```text
If human_label:
    final_label = human_label
Else:
    final_label = predicted_label
```

---

## 📊 Evaluation Metrics

- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1 Score
- Confusion Matrix

⚠️ Note: Dataset is **imbalanced (more positives)**

---

## 🌍 Language Detection

Classifies reviews into:

- english
- non_english
- unknown

Helps improve model reliability.

---

## 📸 Visual Outputs

### 📊 Label Distribution

![Label Distribution](assets/label_distribution.png)

### 📉 Agreement vs Conflict

![Agreement](assets/match_vs_mismatch.png)

---

## 🔍 Example Output

| Clean Text         | Weak     | Predicted | Match |
| ------------------ | -------- | --------- | ----- |
| excelente producto | positive | neutral   | ❌    |
| great product      | positive | positive  | ✅    |

---

## 🛠 Tech Stack

| Tool         | Purpose         |
| ------------ | --------------- |
| Python       | Core            |
| Pandas       | Data processing |
| TextBlob     | Sentiment       |
| VADER        | Sentiment       |
| LangDetect   | Language        |
| Scikit-learn | Metrics         |
| Matplotlib   | Visualization   |

---

## 📁 Project Structure

```text
ai-data-trainer-pipeline/
├── data/
├── docs/
├── src/
├── assets/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Pipeline

```bash
python run_pipeline.py
```

---

## 📊 Outputs

- final_reviews.csv
- uncertain_reviews.csv
- rating_prediction_conflicts.csv
- evaluation_metrics.csv
- final_approved_reviews.csv

---

## 💡 Key Learnings

- Real-world data is noisy
- Ratings ≠ truth
- Hybrid models perform better
- Human validation is essential
- Error analysis improves systems

---

## 🎯 Skills Demonstrated

- Data preprocessing
- Weak labeling
- NLP sentiment analysis
- Model evaluation
- HITL system design
- AI data quality workflows

---

## 🏁 Final Outcome

A **production-style AI pipeline** that:

- Handles noisy labels
- Detects conflicts
- Uses hybrid models
- Integrates human review
- Produces high-quality datasets

---

## 👤 Author

**Nahian Bin Rahman**
🔗 https://github.com/nahian-binrahman

---

<p align="center">
⭐ If you found this useful, consider giving it a star!
</p>
