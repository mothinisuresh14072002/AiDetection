from aidetection.core import MediaType, analyze_bytes, detect_media_type


def test_detect_image():
    assert detect_media_type("photo.jpg") is MediaType.IMAGE


def test_detect_audio():
    assert detect_media_type("voice.wav") is MediaType.AUDIO


def test_detect_video():
    assert detect_media_type("clip.mp4") is MediaType.VIDEO


def test_content_type_wins():
    assert detect_media_type("unknown.bin", "image/png") is MediaType.IMAGE


def test_analyze_bytes():
    result = analyze_bytes(b"data", MediaType.IMAGE)
    assert result.media_type is MediaType.IMAGE
    assert result.ai_probability == 0.5


def test_gif_signature_is_image():
    from aidetection.media import sniff_media_type

    assert sniff_media_type(b"GIF89a" + b"data") is MediaType.IMAGE
