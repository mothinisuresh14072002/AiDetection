import csv
from pathlib import Path

import pytest

from scripts.evaluate import evaluate


def write_manifest(tmp_path: Path, rows: list[dict[str, str]]) -> Path:
    path = tmp_path / "manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["label", "ai_probability"])
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_evaluate_binary_manifest(tmp_path):
    path = write_manifest(
        tmp_path,
        [
            {"label": "real", "ai_probability": "0.1"},
            {"label": "synthetic", "ai_probability": "0.9"},
            {"label": "real", "ai_probability": "0.2"},
            {"label": "synthetic", "ai_probability": "0.8"},
        ],
    )
    result = evaluate(path)
    assert result["f1"] == 1.0
    assert result["roc_auc"] == 1.0


def test_empty_manifest_rejected(tmp_path):
    path = write_manifest(tmp_path, [])
    with pytest.raises(ValueError, match="empty"):
        evaluate(path)
