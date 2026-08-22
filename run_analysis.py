from __future__ import annotations

import json

import pandas as pd

from config import OUTPUT_DIR, PROCESSED_DIR
from nlp.confidence import confidence_score
from nlp.keywords import keyword_frequency
from nlp.sentiment import analyze_sentiment


def analyze_file(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    text = payload["sections"].get("full_document", "")
    sentiment = analyze_sentiment(text)
    keywords = keyword_frequency(text)
    confidence = confidence_score(sentiment.polarity, keywords)
    return {
        "company": payload["company"],
        "year": payload["year"],
        "filename": payload["source"],
        "positive": sentiment.positive,
        "negative": sentiment.negative,
        "neutral": sentiment.neutral,
        "polarity": sentiment.polarity,
        "sentences_analyzed": sentiment.sentences_analyzed,
        "confidence": confidence,
        "AI": keywords["AI"],
        "Inflation": keywords["Inflation"],
        "Expansion": keywords["Expansion"],
        "CapEx": keywords["CapEx"],
        "Risk": keywords["Risk"],
    }


def run() -> pd.DataFrame:
    rows = [analyze_file(path) for path in sorted(PROCESSED_DIR.glob("*.json"))]
    df = pd.DataFrame(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / "confidence_index.csv", index=False)
    df.to_excel(OUTPUT_DIR / "confidence_index.xlsx", index=False)
    return df


if __name__ == "__main__":
    frame = run()
    print(f"Analyzed {len(frame)} documents")
