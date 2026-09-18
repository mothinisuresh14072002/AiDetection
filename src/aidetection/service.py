from .core import AnalysisResult, MediaType, analyze_bytes, detect_media_type
from .limits import validate_size
from .media import validate_media_signature


class DetectionService:
    def analyze(
        self, data: bytes, media_type: MediaType, filename: str = ""
    ) -> AnalysisResult:
        return analyze_bytes(data, media_type, filename)

    def analyze_upload(
        self, data: bytes, filename: str, content_type: str | None
    ) -> AnalysisResult:
        validate_size(data)
        media_type = detect_media_type(filename, content_type)
        if media_type is MediaType.UNKNOWN:
            raise ValueError("unsupported or unknown media type")
        validate_media_signature(data, media_type)
        return self.analyze(data, media_type, filename)
