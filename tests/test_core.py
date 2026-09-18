import pytest
from src.aidetection.core import MediaType, analyze_bytes, detect_media_type

def test_detect_image():
    assert detect_media_type("photo.jpg", "image/jpeg") is MediaType.IMAGE

def test_detect_audio():
    assert detect_media_type("voice.wav", "audio/wav") is MediaType.AUDIO

def test_detect_video():
    assert detect_media_type("clip.mp4", "video/mp4") is MediaType.VIDEO

def test_empty_payload_rejected():
    with pytest.raises(ValueError):
        analyze_bytes(b"", MediaType.IMAGE)

def test_baseline_is_explicit():
    result = analyze_bytes(b"x", MediaType.VIDEO)
    assert result.label == "undetermined"
    assert result.confidence == 0.0
