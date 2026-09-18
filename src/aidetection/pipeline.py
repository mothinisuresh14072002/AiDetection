from .core import AnalysisResult, MediaType
from .provenance import inspect_metadata
from .scoring import classify

def analyze(data: bytes, media_type: MediaType) -> AnalysisResult:
    if not data:
        raise ValueError("media payload is empty")
    provenance=inspect_metadata(data)
    # Conservative until trained, validated model weights are installed.
    score=classify(0.5)
    signals=provenance.signals + score.rationale + ("trained_detector_not_configured",)
    return AnalysisResult(media_type, score.label, score.confidence, signals)
