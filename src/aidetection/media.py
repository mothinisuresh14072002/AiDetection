"""Lightweight media signature validation without decoding untrusted payloads."""

from .core import MediaType


def sniff_media_type(data: bytes) -> MediaType:
    if len(data) < 4:
        return MediaType.UNKNOWN
    head = data[:16]
    if head.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"GIF87a", b"GIF89a")):
        return MediaType.IMAGE
    if head.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return MediaType.IMAGE
    if head.startswith(b"RIFF") and data[8:12] == b"WAVE":
        return MediaType.AUDIO
    if head.startswith(b"RIFF") and data[8:12] == b"AVI ":
        return MediaType.VIDEO
    if head.startswith((b"ID3", b"OggS", b"fLaC")):
        return MediaType.AUDIO
    if head.startswith(b"\x1a\x45\xdf\xa3"):
        return MediaType.VIDEO
    if len(data) >= 12 and data[4:8] == b"ftyp":
        return MediaType.VIDEO
    return MediaType.UNKNOWN


def validate_media_signature(data: bytes, declared: MediaType) -> None:
    actual = sniff_media_type(data)
    if actual is MediaType.UNKNOWN:
        raise ValueError("media signature could not be recognized")
    if actual is not declared:
        raise ValueError(
            f"media signature mismatch: declared {declared.value}, detected {actual.value}"
        )
