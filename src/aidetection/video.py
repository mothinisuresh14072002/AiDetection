"""Bounded video frame sampling bridge for image detectors."""

import tempfile
from pathlib import Path
from statistics import mean


def sample_video_frames(data: bytes, max_frames: int = 12, filename: str = ""):
    if max_frames < 1:
        raise ValueError("max_frames must be at least 1")
    import cv2

    suffix = Path(filename).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as handle:
        handle.write(data)
        handle.flush()
        capture = cv2.VideoCapture(handle.name)
        if not capture.isOpened():
            capture.release()
            raise ValueError("video decoder could not open the uploaded media")
        total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []
        if total > 0:
            targets = {min(total - 1, round(i * (total - 1) / max(1, max_frames - 1))) for i in range(max_frames)}
            index = 0
            while len(frames) < max_frames:
                ok, frame = capture.read()
                if not ok:
                    break
                if index in targets:
                    frames.append(frame)
                index += 1
        else:
            while len(frames) < max_frames:
                ok, frame = capture.read()
                if not ok:
                    break
                frames.append(frame)
        capture.release()
        if not frames:
            raise ValueError("video contains no decodable frames")
        return frames


def aggregate_probabilities(probabilities: list[float]) -> float:
    return mean(probabilities) if probabilities else 0.5
