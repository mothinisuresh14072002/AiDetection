from .core import MediaType, AnalysisResult, detect_media_type, analyze_bytes

class DetectionService:
    def analyze(self, data: bytes, media_type: MediaType) -> AnalysisResult:
        return analyze_bytes(data, media_type)

    def analyze_upload(self, data: bytes, filename: str, content_type: str | None):
        media_type=detect_media_type(filename, content_type)
        if media_type is MediaType.UNKNOWN:
            raise ValueError("unsupported or unknown media type")
        return self.analyze(data, media_type)
