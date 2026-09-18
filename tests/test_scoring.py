from aidetection.scoring import classify


def test_high_score():
    assert classify(0.9).label == "AI_GENERATED"


def test_low_score():
    assert classify(0.1).label == "REAL"


def test_boundary():
    assert classify(0.5).label == "UNCERTAIN"
