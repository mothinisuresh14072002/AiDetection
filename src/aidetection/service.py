from .core import AnalysisResult, MediaType
from .detectors import BaselineDetector

class DetectionService:
    def __init__(self, detector=None):
        self.detector = detector or BaselineDetector()

    def analyze(self, data: bytes, media_type: MediaType) -> AnalysisResult:
        return self.detector.analyze(data, media_type)
