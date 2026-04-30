import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

input_file = "data/labeled_reviews.csv"
output_file = "data/final_reviews.csv"
uncertain_output_file = "data/uncertain_reviews.csv"
metrics_output_file = "data/evaluation_metrics.csv"
confusion_matrix_output_file = "data/confusion_matrix.csv"
classification_report_output_file = "data/classification_report.csv"

# Load data
df = pd.read_csv(input_file)

# Labels used for evaluation
labels = ["positive", "neutral", "negative"]

# --------------------------------------------------
# STEP 1: Separate uncertain predictions
# --------------------------------------------------
uncertain_df = df[df["predicted_label"] == "uncertain"].copy()
certain_df = df[df["predicted_label"] != "uncertain"].copy()

uncertain_df.to_csv(uncertain_output_file, index=False)

# --------------------------------------------------
# STEP 2: Add agreement/conflict columns
# --------------------------------------------------
certain_df["rating_prediction_agreement"] = (
    certain_df["weak_rating_label"] == certain_df["predicted_label"]
)

certain_df["rating_prediction_conflict"] = (
    certain_df["weak_rating_label"] != certain_df["predicted_label"]
)

# --------------------------------------------------
# STEP 3: Counts
# --------------------------------------------------
total_reviews_original = len(df)
total_reviews_after_removing_uncertain = len(certain_df)
uncertain_count = len(uncertain_df)

agreement_count = certain_df["rating_prediction_agreement"].sum()
conflict_count = certain_df["rating_prediction_conflict"].sum()

uncertain_percentage = (
    (uncertain_count / total_reviews_original) * 100
    if total_reviews_original > 0
    else 0
)

coverage_percentage = (
    (total_reviews_after_removing_uncertain / total_reviews_original) * 100
    if total_reviews_original > 0
    else 0
)

agreement_percentage = (
    (agreement_count / total_reviews_after_removing_uncertain) * 100
    if total_reviews_after_removing_uncertain > 0
    else 0
)

conflict_percentage = (
    (conflict_count / total_reviews_after_removing_uncertain) * 100
    if total_reviews_after_removing_uncertain > 0
    else 0
)

# --------------------------------------------------
# STEP 4: Metrics excluding uncertain predictions
# --------------------------------------------------
# These metrics are calculated only on confident/certain predictions.
# They are compared against weak labels, not true human labels.

if total_reviews_after_removing_uncertain > 0:
    y_true_certain = certain_df["weak_rating_label"]
    y_pred_certain = certain_df["predicted_label"]

    accuracy_without_uncertain = accuracy_score(y_true_certain, y_pred_certain)

    precision_without_uncertain = precision_score(
        y_true_certain,
        y_pred_certain,
        labels=labels,
        average="weighted",
        zero_division=0,
    )

    recall_without_uncertain = recall_score(
        y_true_certain,
        y_pred_certain,
        labels=labels,
        average="weighted",
        zero_division=0,
    )

    f1_without_uncertain = f1_score(
        y_true_certain,
        y_pred_certain,
        labels=labels,
        average="weighted",
        zero_division=0,
    )
else:
    accuracy_without_uncertain = 0
    precision_without_uncertain = 0
    recall_without_uncertain = 0
    f1_without_uncertain = 0

# --------------------------------------------------
# STEP 5: Metrics including uncertain as model failure
# --------------------------------------------------
# This gives a more realistic view because uncertain predictions
# are counted as not matching the weak label.

df_with_uncertain_eval = df.copy()

df_with_uncertain_eval["prediction_for_eval"] = df_with_uncertain_eval[
    "predicted_label"
].replace("uncertain", "unclassified")

all_eval_labels = ["positive", "neutral", "negative", "unclassified"]

y_true_all = df_with_uncertain_eval["weak_rating_label"]
y_pred_all = df_with_uncertain_eval["prediction_for_eval"]

accuracy_with_uncertain = accuracy_score(y_true_all, y_pred_all)

precision_with_uncertain = precision_score(
    y_true_all,
    y_pred_all,
    labels=all_eval_labels,
    average="weighted",
    zero_division=0,
)

recall_with_uncertain = recall_score(
    y_true_all,
    y_pred_all,
    labels=all_eval_labels,
    average="weighted",
    zero_division=0,
)

f1_with_uncertain = f1_score(
    y_true_all,
    y_pred_all,
    labels=all_eval_labels,
    average="weighted",
    zero_division=0,
)

# --------------------------------------------------
# STEP 6: Confusion matrix without uncertain
# --------------------------------------------------
cm = confusion_matrix(
    certain_df["weak_rating_label"],
    certain_df["predicted_label"],
    labels=labels,
)

cm_df = pd.DataFrame(
    cm,
    index=[f"weak_actual_{label}" for label in labels],
    columns=[f"predicted_{label}" for label in labels],
)

cm_df.to_csv(confusion_matrix_output_file)

# --------------------------------------------------
# STEP 7: Classification report without uncertain
# --------------------------------------------------
report_dict = classification_report(
    certain_df["weak_rating_label"],
    certain_df["predicted_label"],
    labels=labels,
    output_dict=True,
    zero_division=0,
)

report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv(classification_report_output_file)

# --------------------------------------------------
# STEP 8: Save metrics summary
# --------------------------------------------------
metrics_df = pd.DataFrame(
    {
        "metric": [
            "total_reviews_original",
            "total_reviews_after_removing_uncertain",
            "uncertain_reviews",
            "uncertain_percentage",
            "coverage_percentage",
            "agreement_count_with_weak_labels",
            "conflict_count_with_weak_labels",
            "agreement_percentage_without_uncertain",
            "conflict_percentage_without_uncertain",
            "accuracy_without_uncertain_vs_weak_labels",
            "weighted_precision_without_uncertain_vs_weak_labels",
            "weighted_recall_without_uncertain_vs_weak_labels",
            "weighted_f1_without_uncertain_vs_weak_labels",
            "accuracy_with_uncertain_counted_as_unclassified",
            "weighted_precision_with_uncertain_counted_as_unclassified",
            "weighted_recall_with_uncertain_counted_as_unclassified",
            "weighted_f1_with_uncertain_counted_as_unclassified",
        ],
        "value": [
            total_reviews_original,
            total_reviews_after_removing_uncertain,
            uncertain_count,
            round(uncertain_percentage, 2),
            round(coverage_percentage, 2),
            agreement_count,
            conflict_count,
            round(agreement_percentage, 2),
            round(conflict_percentage, 2),
            round(accuracy_without_uncertain, 4),
            round(precision_without_uncertain, 4),
            round(recall_without_uncertain, 4),
            round(f1_without_uncertain, 4),
            round(accuracy_with_uncertain, 4),
            round(precision_with_uncertain, 4),
            round(recall_with_uncertain, 4),
            round(f1_with_uncertain, 4),
        ],
    }
)

metrics_df.to_csv(metrics_output_file, index=False)

# --------------------------------------------------
# STEP 9: Save final evaluated dataset
# --------------------------------------------------
certain_df.to_csv(output_file, index=False)

# --------------------------------------------------
# PRINT SUMMARY
# --------------------------------------------------
print("Evaluation Completed")
print("--------------------")
print("Weak labels are used as reference labels, not absolute ground truth.")
print()
print(f"Total original reviews: {total_reviews_original}")
print(f"Reviews after removing uncertain: {total_reviews_after_removing_uncertain}")
print(f"Uncertain predictions: {uncertain_count}")
print(f"Uncertain percentage: {uncertain_percentage:.2f}%")
print(f"Prediction coverage: {coverage_percentage:.2f}%")
print()
print(f"Agreement with weak labels: {agreement_count}")
print(f"Conflict with weak labels: {conflict_count}")
print(f"Agreement percentage without uncertain: {agreement_percentage:.2f}%")
print(f"Conflict percentage without uncertain: {conflict_percentage:.2f}%")
print()
print("Metrics WITHOUT uncertain predictions:")
print(f"Accuracy: {accuracy_without_uncertain:.4f}")
print(f"Weighted Precision: {precision_without_uncertain:.4f}")
print(f"Weighted Recall: {recall_without_uncertain:.4f}")
print(f"Weighted F1 Score: {f1_without_uncertain:.4f}")
print()
print("Metrics WITH uncertain counted as unclassified:")
print(f"Accuracy: {accuracy_with_uncertain:.4f}")
print(f"Weighted Precision: {precision_with_uncertain:.4f}")
print(f"Weighted Recall: {recall_with_uncertain:.4f}")
print(f"Weighted F1 Score: {f1_with_uncertain:.4f}")
print()
print("Files saved successfully:")
print(f"Final reviews: {output_file}")
print(f"Uncertain reviews: {uncertain_output_file}")
print(f"Evaluation metrics: {metrics_output_file}")
print(f"Confusion matrix: {confusion_matrix_output_file}")
print(f"Classification report: {classification_report_output_file}")
