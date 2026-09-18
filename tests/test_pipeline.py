from src.aidetection.core import MediaType
from src.aidetection.pipeline import analyze


def test_baseline_is_conservative(monkeypatch):
    monkeypatch.delenv("AIDETECTION_ENABLE_MODELS", raising=False)
    result = analyze(b"data", MediaType.IMAGE)
    assert result.label == "UNCERTAIN"
    assert "trained_detector_not_configured" in result.signals
