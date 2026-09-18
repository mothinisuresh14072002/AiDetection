"""Pluggable detector interfaces and conservative baseline signals."""
from dataclasses import dataclass
from .core import AnalysisResult, MediaType

@dataclass(frozen=True)
class Signal:
    name: str
    value: float
    description: str

class Detector:
    name = "base"
    def analyze(self, data: bytes, media_type: MediaType) -> AnalysisResult:
        raise NotImplementedError

class BaselineDetector(Detector):
    name = "baseline"
    def analyze(self, data: bytes, media_type: MediaType) -> AnalysisResult:
        if not data:
            raise ValueError("media payload is empty")
        return AnalysisResult(
            media_type=media_type,
            label="undetermined",
            confidence=0.0,
            signals=("no production model configured",),
        )
