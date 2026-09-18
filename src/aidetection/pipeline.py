import os
import os.path

from .core import AnalysisResult, MediaType
from .models import predict_audio, predict_image
from .provenance import inspect_metadata
from .scoring import classify


def analyze(data: bytes, media_type: MediaType, filename: str = "") -> AnalysisResult:
    if not data:
        raise ValueError("media payload is empty")
    provenance = inspect_metadata(data)
    signals = list(provenance.signals)
    use_models = os.getenv("AIDETECTION_ENABLE_MODELS", "0") == "1"
    if not use_models:
        score = classify(0.5)
        signals.extend(score.rationale)
        signals.append("trained_detector_not_configured")
        return AnalysisResult(media_type, score.label, score.confidence, tuple(signals), score.ai_probability)
    try:
        if media_type is MediaType.IMAGE:
            probability = predict_image(data)
        elif media_type is MediaType.AUDIO:
            probability = predict_audio(data, os.path.splitext(filename)[1] or ".wav")
        else:
            import cv2

            from .video import aggregate_probabilities, sample_video_frames

            probabilities = []
            for frame in sample_video_frames(data, filename=filename):
                ok, encoded = cv2.imencode(".jpg", frame)
                if ok:
                    probabilities.append(predict_image(encoded.tobytes()))
            if not probabilities:
                raise ValueError("video could not be decoded into analyzable frames")
            probability = aggregate_probabilities(probabilities)
            signals.append(f"sampled_frames={len(probabilities)}")
        score = classify(probability)
        signals.extend(score.rationale)
        signals.append("optional_huggingface_model")
        return AnalysisResult(media_type, score.label, score.confidence, tuple(signals), score.ai_probability)
    except ImportError as exc:
        raise RuntimeError(
            "model inference dependencies are missing; install the models extra"
        ) from exc
