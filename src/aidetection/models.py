"""Optional Hugging Face model adapters with explicit, model-specific label handling."""

import os
import tempfile
from functools import lru_cache
from io import BytesIO
from pathlib import Path

IMAGE_MODEL = os.getenv("AIDETECTION_IMAGE_MODEL", "Reju983/ai-generated-image-detector")
AUDIO_MODEL = os.getenv("AIDETECTION_AUDIO_MODEL", "garystafford/wav2vec2-deepfake-voice-detector")


def _labels(name: str, default: str) -> frozenset[str]:
    return frozenset(
        token.strip().lower()
        for token in os.getenv(name, default).split(",")
        if token.strip()
    )


IMAGE_FAKE_LABELS = _labels("AIDETECTION_IMAGE_FAKE_LABELS", "ai-generated,fake,generated,synthetic")
AUDIO_FAKE_LABELS = _labels("AIDETECTION_AUDIO_FAKE_LABELS", "fake,deepfake,spoof,synthetic,ai")


def _probability(items, fake_labels) -> float:
    scores = [
        (str(item.get("label", "")).strip().lower(), float(item.get("score", 0.0)))
        for item in items
    ]
    total = sum(max(score, 0.0) for _, score in scores)
    if not total:
        return 0.5
    fake = sum(max(score, 0.0) for label, score in scores if label in fake_labels)
    return max(0.0, min(1.0, fake / total))


@lru_cache(maxsize=2)
def _image_pipeline():
    from transformers import pipeline
    return pipeline("image-classification", model=IMAGE_MODEL)


@lru_cache(maxsize=2)
def _audio_pipeline():
    from transformers import pipeline
    return pipeline("audio-classification", model=AUDIO_MODEL)


def predict_image(data: bytes) -> float:
    from PIL import Image
    image = Image.open(BytesIO(data)).convert("RGB")
    return _probability(_image_pipeline()(image), IMAGE_FAKE_LABELS)


def predict_audio(data: bytes, suffix: str = ".wav") -> float:
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as handle:
        handle.write(data)
        path = Path(handle.name)
    try:
        return _probability(_audio_pipeline()(str(path)), AUDIO_FAKE_LABELS)
    finally:
        path.unlink(missing_ok=True)
