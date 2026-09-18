"""Video frame sampling bridge for image detectors."""

import tempfile
from statistics import mean


def sample_video_frames(data: bytes, max_frames: int = 12, filename: str = ""):
    import cv2

    suffix = ".mp4"
    if filename:
        from pathlib import Path

        suffix = Path(filename).suffix or suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as handle:
        handle.write(data)
        handle.flush()
        capture = cv2.VideoCapture(handle.name)
        total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(1, total // max_frames) if total else 1
        index = 0
        frames = []
        while len(frames) < max_frames:
            ok, frame = capture.read()
            if not ok:
                break
            if index % step == 0:
                frames.append(frame)
            index += 1
        capture.release()
        return frames


def aggregate_probabilities(probabilities: list[float]) -> float:
    return mean(probabilities) if probabilities else 0.5
