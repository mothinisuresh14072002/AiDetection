"""Video frame sampling bridge for image detectors."""
from statistics import mean

def sample_video_frames(data: bytes, max_frames: int = 12):
    import cv2
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=True) as handle:
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
