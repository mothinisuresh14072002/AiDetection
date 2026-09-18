"""Evaluate detector predictions from a CSV manifest."""

import argparse
import csv
from pathlib import Path


def evaluate(path: Path) -> dict[str, float]:
    from sklearn.metrics import (
        average_precision_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("evaluation manifest is empty")
    required = {"label", "ai_probability"}
    if not required.issubset(rows[0]):
        raise ValueError("manifest must contain label and ai_probability columns")
    labels = [
        1 if row["label"].strip().lower() in {"synthetic", "fake", "ai"} else 0
        for row in rows
    ]
    probabilities = [float(row["ai_probability"]) for row in rows]
    if any(not 0 <= p <= 1 for p in probabilities):
        raise ValueError("ai_probability values must be between 0 and 1")
    predicted = [int(p >= 0.5) for p in probabilities]
    result = {
        "precision": precision_score(labels, predicted, zero_division=0),
        "recall": recall_score(labels, predicted, zero_division=0),
        "f1": f1_score(labels, predicted, zero_division=0),
    }
    if len(set(labels)) == 2:
        result["roc_auc"] = roc_auc_score(labels, probabilities)
        result["pr_auc"] = average_precision_score(labels, probabilities)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate AiDetection predictions.")
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    for name, value in evaluate(args.manifest).items():
        print(f"{name}: {value:.4f}")


if __name__ == "__main__":
    main()
