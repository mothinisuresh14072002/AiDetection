"""Conservative conversion of detector probability into a user-facing class."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    label: str
    confidence: float
    rationale: tuple[str, ...]
    ai_probability: float


def classify(ai_probability: float, *, margin: float = 0.15) -> Score:
    """Classify a probability without pretending it is calibrated certainty."""
    p = max(0.0, min(1.0, float(ai_probability)))
    distance = abs(p - 0.5)
    if distance <= margin:
        confidence = min(1.0, distance / margin) if margin > 0 else 0.0
        return Score("UNCERTAIN", confidence, ("model score is close to the decision boundary",), p)
    if p >= 0.8:
        return Score("AI_GENERATED", p, ("strong model evidence leans synthetic; verify independently for high-stakes use",), p)
    if p >= 0.6:
        return Score("LIKELY_AI_GENERATED", p, ("model evidence leans synthetic",), p)
    if p <= 0.2:
        return Score("REAL", 1.0 - p, ("model evidence leans authentic",), p)
    return Score("LIKELY_REAL", 1.0 - p, ("model evidence leans authentic",), p)
