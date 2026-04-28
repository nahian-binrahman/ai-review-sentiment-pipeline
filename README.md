📌 **Project Title**

**AI-Assisted Sentiment Labeling Pipeline with Ground Truth Validation and Error Analysis**

🧭 Project Overview

This project builds an end-to-end AI data training pipeline for customer reviews.
It cleans raw text data, generates sentiment labels, compares AI predictions with ground truth, and analyzes model errors.

The goal is to simulate real-world work of an AI Data Trainer, focusing on:

Data cleaning
Automated labeling
Label validation
Error analysis
🎯 Key Objectives
Transform messy review data into a clean dataset
Generate two types of sentiment labels
Evaluate AI predictions against ground truth
Identify and analyze model mistakes
Detect data quality issues (e.g., non-English text)
🛠️ Tech Stack
🐍 Python
📦 Pandas – data processing
🧠 TextBlob – sentiment prediction
🧑‍💻 VS Code + Git Bash
📁 Project Structure
ai-review-labeling-pipeline/
│
├── data/
│   ├── raw_reviews.csv
│   ├── processed_reviews.csv
│   ├── labeled_reviews.csv
│   ├── final_reviews.csv
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
│   ├── 07_detect_language_issues.py
│   └── 08_export_reports.py
│
├── README.md
└── requirements.txt
⚙️ Pipeline Workflow
🧹 1. Data Selection
Removed unnecessary columns
Kept only useful features
🧩 2. Text Preparation
Combined title + review
Handled missing values
🧼 3. Text Cleaning
Removed HTML tags (<br>)
Removed special characters and URLs
Converted text to lowercase
🧠 Sentiment Labeling
🔹 Ground Truth (Rating-Based)
Rating	Label
4–5	Positive
3	Neutral
1–2	Negative
🔹 AI Prediction (TextBlob)

TextBlob analyzes text polarity and assigns:

Positive
Neutral
Negative
🔍 Label Comparison

A new column:

label_match

Indicates whether AI prediction matches the rating label.

Example:
rating_label: positive
predicted_label: neutral
label_match: False ❌
📉 Error Analysis

Extracted all mismatched rows into:

portfolio_mismatch_report.csv
Common issues found:
🌐 Non-English reviews
✂️ Very short text
🤔 Ambiguous sentiment
⭐ Rating does not match text tone
🌍 Language Issue Detection

Added:

language_flag

Values:

english_or_unknown
possible_non_english

This helps explain why the AI model fails in some cases.

📊 Final Outputs
📄 portfolio_final_reviews.csv

Complete dataset with:

Cleaned text
Labels
Match results
Language flags
⚠️ portfolio_mismatch_report.csv

Only incorrect predictions (AI mistakes)

📈 portfolio_summary_report.csv

Key metrics:

Total reviews
Match percentage
Mismatch percentage
Label distribution
Language distribution
🔎 Sample Insight

Example mismatch:

Text: excelentes a mi esposo le encantan
Rating: 5 (positive)
AI Prediction: neutral ❌
Reason: Non-English text
💡 Key Learnings
AI models can fail due to data quality issues
Non-English text affects sentiment prediction
Rating-based labels work as ground truth
Error analysis is critical in AI workflows
🎯 Skills Demonstrated
🧹 Data cleaning and preprocessing
🏷️ Automated data labeling
🔍 AI output evaluation
⚠️ Error detection and analysis
📊 Dataset quality assessment
🚀 How to Run
pip install -r requirements.txt

Run the pipeline:

python src/01_load_and_select.py
python src/02_prepare_text.py
python src/03_clean_text.py
python src/04_create_labels.py
python src/05_compare_labels.py
python src/06_analyze_mistakes.py
python src/07_detect_language_issues.py
python src/08_export_reports.py
🏁 Final Result

This project demonstrates a complete workflow of an AI Data Trainer, including:

✔ Data preparation
✔ Automated labeling
✔ Model evaluation
✔ Error analysis
✔ Data quality inspection