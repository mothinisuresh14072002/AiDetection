from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    label: str
    confidence: float
    rationale: tuple[str, ...]


def classify(ai_probability: float, *, margin: float = 0.15) -> Score:
    p = max(0.0, min(1.0, float(ai_probability)))
    if 0.5 - margin <= p <= 0.5 + margin:
        return Score(
            "UNCERTAIN", 1.0 - abs(p - 0.5) * 2, ("score is near decision boundary",)
        )
    if p >= 0.8:
        return Score(
            "AI_GENERATED",
            p,
            ("multiple signals should be confirmed before high-stakes use",),
        )
    if p >= 0.6:
        return Score("LIKELY_AI_GENERATED", p, ("model evidence leans synthetic",))
    if p <= 0.2:
        return Score("REAL", 1.0 - p, ("model evidence leans authentic",))
    return Score("LIKELY_REAL", 1.0 - p, ("model evidence leans authentic",))
