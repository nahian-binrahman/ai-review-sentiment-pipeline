# Sentiment Annotation Guidelines

This document defines how customer reviews should be labeled for sentiment analysis.

The goal is to ensure **consistent, accurate, and high-quality labels** for AI training and evaluation.

---

## 🎯 Label Categories

Each review must be assigned **one** label:

- **Positive**
- **Neutral**
- **Negative**

---

## ✅ Positive

### Definition
The review clearly shows **satisfaction, happiness, or approval**.

### Examples

| Review Text | Label | Reason |
|---|---|---|
| "This product is amazing" | Positive | Clear praise |
| "Works perfectly" | Positive | User is satisfied |
| "Excellent quality" | Positive | Strong positive opinion |

### Rules

- Strong positive words → Positive  
- Clear recommendation → Positive  
- Short positive text like "good", "great" → Positive  

---

## 😐 Neutral

### Definition
The review is **mixed, unclear, or informational**, without strong emotion.

### Examples

| Review Text | Label | Reason |
|---|---|---|
| "It is okay" | Neutral | Mild opinion |
| "Received the product yesterday" | Neutral | Informational |
| "Not bad, not great" | Neutral | Mixed sentiment |

### Rules

- No strong positive or negative feeling → Neutral  
- Mixed opinions → Neutral (unless one side dominates)  
- Factual statements → Neutral  

---

## ❌ Negative

### Definition
The review shows **complaint, dissatisfaction, or disappointment**.

### Examples

| Review Text | Label | Reason |
|---|---|---|
| "Terrible product" | Negative | Clear complaint |
| "Waste of money" | Negative | Strong negative opinion |
| "Stopped working after one day" | Negative | Bad experience |

### Rules

- Complaints → Negative  
- Strong negative words → Negative  
- Short negative text like "bad", "poor" → Negative  

---

## ⚠️ Edge Cases

These rules handle tricky situations.

---

### 🔁 Mixed Sentiment

If a review contains both positive and negative:

| Review Text | Label | Reason |
|---|---|---|
| "Good quality but too expensive" | Neutral | Balanced sentiment |
| "Nice design but broke quickly" | Negative | Negative issue dominates |

**Rule:**
- Balanced → Neutral  
- Negative dominates → Negative  
- Positive dominates → Positive  

---

### 🤔 Sarcasm

Interpret **actual meaning**, not just words.

| Review Text | Label | Reason |
|---|---|---|
| "Great, it broke in 2 days" | Negative | Sarcastic complaint |

---

### ✂️ Very Short Text

| Review Text | Label |
|---|---|
| "Good" | Positive |
| "Bad" | Negative |
| "Ok" | Neutral |

**Rule:**
- If meaning is unclear → mark as **uncertain** (optional system label)

---

### 🌍 Non-English Text

| Review Text | Label | Reason |
|---|---|---|
| "excelente producto" | Positive | Means excellent product |
| "muy malo" | Negative | Means very bad |

**Rule:**
- If meaning is understood → label normally  
- If unclear → mark for **manual review**  

---

### 📦 No Sentiment / Informational

| Review Text | Label |
|---|---|
| "Arrived on Monday" | Neutral |
| "Package received" | Neutral |

---

## 🧪 Uncertain Cases

Use **uncertain** when:

- Text is too short or unclear  
- Meaning cannot be determined  
- Mixed language or ambiguous meaning  

These cases should be sent to **human review**.

---

## 🔁 Human Review Rules

Send a review for human review if:

- Model confidence is **low**  
- Prediction and rating **do not match**  
- Text is **non-English or unclear**  
- Contains **sarcasm or mixed sentiment**  

---

## 🏷️ Confidence Levels

Each prediction can include a confidence level:

| Score | Confidence |
|------|-----------|
| High | Strong sentiment |
| Medium | Moderate sentiment |
| Low | Weak or unclear sentiment |

---

## ❗ Common Mistakes to Avoid

- Do not rely only on keywords  
- Do not ignore context  
- Do not mislabel sarcasm  
- Do not force a label when uncertain  

---

## 📌 Summary

These guidelines ensure:

- Consistent labeling  
- Better training data quality  
- Improved AI performance  
- Reliable evaluation results  

