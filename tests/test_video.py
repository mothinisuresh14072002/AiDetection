import pytest

from aidetection.video import aggregate_probabilities, sample_video_frames


def test_aggregate_empty_is_neutral():
    assert aggregate_probabilities([]) == 0.5


def test_aggregate_mean():
    assert aggregate_probabilities([0.2, 0.8]) == 0.5


def test_sample_rejects_invalid_frame_limit():
    with pytest.raises(ValueError, match="at least 1"):
        sample_video_frames(b"data", max_frames=0)
