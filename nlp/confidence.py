from __future__ import annotations


def _minmax(value: float, scale: float = 50.0) -> float:
    return min(1.0, value / scale) if scale else 0.0


def calculate_confidence(sentiment: dict, keywords: dict[str, int]) -> float:
    positive = float(sentiment.get("positive", 0.0))
    negative = float(sentiment.get("negative", 0.0))

    expansion = _minmax(keywords.get("Expansion", 0), 25)
    capex = _minmax(keywords.get("CapEx", 0), 25)
    ai = _minmax(keywords.get("AI", 0), 25)
    inflation = _minmax(keywords.get("Inflation", 0), 15)
    risk = _minmax(keywords.get("Risk", 0), 20)

    raw = (
        50
        + 25 * (positive - negative)
        + 12 * expansion
        + 8 * capex
        + 5 * ai
        - 7 * inflation
        - 13 * risk
    )
    return round(max(0.0, min(100.0, raw)), 2)
