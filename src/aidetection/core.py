from dataclasses import dataclass
from enum import Enum

class MediaType(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class AnalysisResult:
    media_type: MediaType
    label: str
    confidence: float
    signals: tuple[str, ...]

def detect_media_type(filename: str, content_type: str | None = None) -> MediaType:
    value=(content_type or "").lower()
    name=filename.lower()
    if value.startswith("image/") or name.endswith((".jpg",".jpeg",".png",".webp",".gif")):
        return MediaType.IMAGE
    if value.startswith("audio/") or name.endswith((".wav",".mp3",".m4a",".flac",".ogg")):
        return MediaType.AUDIO
    if value.startswith("video/") or name.endswith((".mp4",".mov",".webm",".mkv",".avi")):
        return MediaType.VIDEO
    return MediaType.UNKNOWN

def analyze_bytes(data: bytes, media_type: MediaType) -> AnalysisResult:
    from .pipeline import analyze
    return analyze(data, media_type)
