"""Optional Hugging Face model adapters."""
import os
from functools import lru_cache

IMAGE_MODEL = os.getenv("AIDETECTION_IMAGE_MODEL", "Reju983/ai-generated-image-detector")
AUDIO_MODEL = os.getenv("AIDETECTION_AUDIO_MODEL", "garystafford/wav2vec2-deepfake-voice-detector")

@lru_cache(maxsize=2)
def _image_pipeline():
    from transformers import pipeline
    return pipeline("image-classification", model=IMAGE_MODEL)

@lru_cache(maxsize=2)
def _audio_pipeline():
    from transformers import pipeline
    return pipeline("audio-classification", model=AUDIO_MODEL)

def _fake_probability(items) -> float:
    fake = 0.0
    total = 0.0
    for item in items:
        label = str(item.get("label", "")).lower()
        score = float(item.get("score", 0.0))
        total += score
        if any(token in label for token in ("fake", "ai", "synthetic", "spoof", "generated")):
            fake += score
    return fake / total if total else 0.5

def predict_image(data: bytes) -> float:
    from io import BytesIO
    from PIL import Image
    image = Image.open(BytesIO(data)).convert("RGB")
    return _fake_probability(_image_pipeline()(image))

def predict_audio(data: bytes, suffix: str = ".wav") -> float:
    import tempfile
    from pathlib import Path
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
        handle.write(data)
        path = Path(handle.name)
    try:
        return _fake_probability(_audio_pipeline()(str(path)))
    finally:
        path.unlink(missing_ok=True)
