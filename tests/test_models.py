from aidetection.models import _probability


def test_probability_uses_explicit_labels():
    items = [{"label": "real", "score": 0.25}, {"label": "fake", "score": 0.75}]
    assert _probability(items) == 0.75


def test_unknown_labels_are_not_assumed_fake():
    items = [{"label": "class_0", "score": 0.7}, {"label": "class_1", "score": 0.3}]
    assert _probability(items) == 0.0
