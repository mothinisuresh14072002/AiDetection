from src.aidetection.scoring import classify
def test_high_score():
    assert classify(.9).label=="AI_GENERATED"
def test_low_score():
    assert classify(.1).label=="REAL"
def test_boundary():
    assert classify(.5).label=="UNCERTAIN"
