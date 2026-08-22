import re

KEYWORDS = {
    "AI": ["artificial intelligence", "generative ai", "genai", "llm", "automation", "machine learning"],
    "Inflation": ["inflation", "commodity prices", "cost pressure", "input costs"],
    "Expansion": ["expansion", "capacity expansion", "new plant", "new facility", "geographic expansion"],
    "CapEx": ["capex", "capital expenditure", "capital expenditures", "capital investment"],
    "Risk": ["risk", "uncertainty", "slowdown", "volatility", "headwinds"],
}


def keyword_frequency(text: str) -> dict[str, int]:
    text_lower = text.lower()
    result: dict[str, int] = {}
    for category, terms in KEYWORDS.items():
        result[category] = sum(
            len(re.findall(r"\b" + re.escape(term) + r"\b", text_lower))
            for term in terms
        )
    return result
