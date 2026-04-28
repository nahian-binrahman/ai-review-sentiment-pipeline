# 📊 AI-Assisted Sentiment Labeling Pipeline with Ground Truth Validation and Error Analysis

## 🚀 What This Project Shows

- Built a complete **AI data training pipeline**
- Compared **AI predictions vs ground truth labels**
- Identified **model weaknesses** such as non-English text and short reviews
- Performed **real-world error analysis**

---

## 🧭 Project Overview

This project simulates the workflow of an **AI Data Trainer**.

It processes raw customer reviews and performs:

- Data cleaning
- Sentiment labeling
- AI evaluation
- Error analysis
- Data quality inspection

---

## 🖼️ Demo

### Pipeline Output

![Pipeline Demo](assets/demo_pipeline.png)

### AI Mistake Example

![Mismatch Example](assets/demo_mismatch.png)

### Before → After → Label → Result

```text
Before:
"The product is AMAZING!!! 😍😍 <br>"

After:
"the product is amazing"

rating_label: positive
predicted_label: positive

Result: Match ✅
```

### AI Mistake Example

```text
Text:
"excelentes a mi esposo le encantan"

rating_label: positive
predicted_label: neutral

Result: Mismatch ❌
Reason: Non-English text
```

---

## 🛠️ Tech Stack

- 🐍 Python
- 📦 Pandas
- 🧠 TextBlob
- 💻 VS Code + Git Bash

---

## 📁 Project Structure

```text
ai-review-labeling-pipeline/
│
├── data/
│   ├── raw_reviews.csv
│   ├── portfolio_final_reviews.csv
│   ├── portfolio_mismatch_report.csv
│   └── portfolio_summary_report.csv
│
├── src/
│   ├── 01_load_and_select.py
│   ├── 02_prepare_text.py
│   ├── 03_clean_text.py
│   ├── 04_create_labels.py
│   ├── 05_compare_labels.py
│   ├── 06_analyze_mistakes.py
│   ├── 06b_add_mistake_reasons.py
│   ├── 07_detect_language_issues.py
│   ├── 07b_create_english_only_dataset.py
│   └── 08_export_reports.py
│
├── assets/
├── README.md
└── requirements.txt
```

---

## ⚙️ Pipeline Workflow

### 🧹 1. Data Selection
- Removed unnecessary columns  
- Kept useful features  

### 🧩 2. Text Preparation
- Combined `title + review`  
- Handled missing values  

### 🧼 3. Text Cleaning
- Removed HTML tags (`<br>`)  
- Removed special characters and URLs  
- Converted text to lowercase  

---

### 🧠 4. Sentiment Labeling

#### Ground Truth (Rating-Based)

| Rating | Label |
|--------|------|
| 4–5 | Positive |
| 3 | Neutral |
| 1–2 | Negative |

#### AI Prediction (TextBlob)

- Uses text polarity  
- Outputs: positive / neutral / negative  

---

### 🔍 5. Label Comparison

Created:

```text
label_match
```

Checks:

```text
rating_label == predicted_label
```

---

### 📉 6. Error Analysis

Extracted mismatched rows:

```text
portfolio_mismatch_report.csv
```

---

### 🌍 7. Language Detection

Added:

```text
language_flag
```

Values:
- `english_or_unknown`
- `possible_non_english`

---

### 📊 8. Final Outputs

- 📄 `portfolio_final_reviews.csv` → full dataset  
- ⚠️ `portfolio_mismatch_report.csv` → AI mistakes  
- 📈 `portfolio_summary_report.csv` → summary metrics  

---

## 📊 Sample Insight

```text
Text: excelentes a mi esposo le encantan
Rating: 5 (positive)
AI Prediction: neutral ❌
Reason: Non-English text
```

---

## 📊 Results

### Label Distribution
![Label Distribution](assets/label_distribution.png)

### Prediction Accuracy
![Prediction Accuracy](assets/match_vs_mismatch.png)

## 💡 Key Learnings

- Data quality directly impacts AI performance  
- Non-English text reduces accuracy  
- Rating labels act as ground truth  
- Error analysis is critical in AI workflows  

---

## 🎯 Skills Demonstrated

- 🧹 Data cleaning & preprocessing  
- 🏷️ Automated labeling  
- 🔍 AI evaluation  
- ⚠️ Error analysis  
- 📊 Dataset quality assessment  

---

## 🚀 How to Run

```bash
pip install -r requirements.txt
```

```bash
python src/01_load_and_select.py
python src/02_prepare_text.py
python src/03_clean_text.py
python src/04_create_labels.py
python src/05_compare_labels.py
python src/06_analyze_mistakes.py
python src/07_detect_language_issues.py
python src/08_export_reports.py
```

---

## 🏁 Final Result

This project demonstrates a complete workflow of an **AI Data Trainer**, including:

- Data preparation  
- Automated labeling  
- Model evaluation  
- Error analysis  
- Data quality inspection  

---

