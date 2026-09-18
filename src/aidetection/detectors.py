"""Pluggable detector interfaces and conservative baseline signals."""

from dataclasses import dataclass

from .core import AnalysisResult, MediaType


@dataclass(frozen=True)
class DetectorMetadata:
    name: str
    version: str
    modality: MediaType


class Detector:
    """Small protocol-like base class for future detector implementations."""

    metadata: DetectorMetadata

    def analyze(self, data: bytes, filename: str = "") -> AnalysisResult:
        raise NotImplementedError
