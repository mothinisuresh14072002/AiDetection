from aidetection.scoring import classify


def test_high_score():
    score = classify(0.9)
    assert score.label == "AI_GENERATED"
    assert score.ai_probability == 0.9


def test_low_score():
    assert classify(0.1).label == "REAL"


def test_boundary_is_uncertain():
    score = classify(0.5)
    assert score.label == "UNCERTAIN"
    assert score.confidence == 0.0


def test_probability_is_clamped():
    assert classify(2).ai_probability == 1.0
    assert classify(-1).ai_probability == 0.0
