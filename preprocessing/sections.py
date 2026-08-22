from __future__ import annotations

import re

SECTION_ALIASES = {
    "ceo_message": ["ceo message", "chairman's message", "message from the ceo", "message from the chairman"],
    "md&a": ["management discussion and analysis", "management discussion", "md&a"],
    "outlook": ["outlook", "business outlook", "future outlook"],
    "risk": ["risk management", "key risks", "risk factors"],
}


def extract_sections(text: str) -> dict[str, str]:
    lower = text.lower()
    positions: list[tuple[int, str]] = []
    for section, aliases in SECTION_ALIASES.items():
        hits = [lower.find(alias) for alias in aliases if lower.find(alias) >= 0]
        if hits:
            positions.append((min(hits), section))
    positions.sort()
    if not positions:
        return {"full_document": text}

    result: dict[str, str] = {}
    for idx, (start, section) in enumerate(positions):
        end = positions[idx + 1][0] if idx + 1 < len(positions) else len(text)
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        result[section] = snippet[:50000]
    result["full_document"] = text
    return result

