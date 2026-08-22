import json
import re
from pathlib import Path

from config import OUTPUT_DIR, PROCESSED_DIR
from nlp.confidence import calculate_confidence
from nlp.keywords import keyword_frequency
from nlp.sentiment import analyze_sentiment


def parse_metadata(filename: str):
    match = re.match(r"(.+?)_(\d{4})\.txt$", filename)
    if not match:
        return filename.removesuffix(".txt").replace("_", " "), None
    return match.group(1).replace("_", " "), int(match.group(2))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(PROCESSED_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        company, year = parse_metadata(path.name)
        sentiment = analyze_sentiment(text)
        keywords = keyword_frequency(text)
        confidence = calculate_confidence(sentiment, keywords)
        row = {
            "company": company,
            "year": year,
            "confidence": confidence,
            "sentiment_label": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "positive_score": sentiment["positive"],
            "negative_score": sentiment["negative"],
            **{f"{key}_mentions": value for key, value in keywords.items()},
        }
        rows.append(row)
        print(f"Analyzed {company} {year or ''}: confidence={confidence}".strip())

    output = OUTPUT_DIR / "analysis_results.json"
    output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Saved {len(rows)} analysis records to {output}")


if __name__ == "__main__":
    main()
