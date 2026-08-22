from __future__ import annotations


def confidence_score(polarity: float, keywords: dict[str, int]) -> float:
    score = 50.0 + 35.0 * polarity
    score += min(keywords.get("Expansion", 0), 40) * 0.25
    score += min(keywords.get("CapEx", 0), 40) * 0.20
    score += min(keywords.get("AI", 0), 40) * 0.10
    score -= min(keywords.get("Risk", 0), 40) * 0.30
    score -= min(keywords.get("Inflation", 0), 40) * 0.15
    return round(max(0.0, min(100.0, score)), 2)
