from functools import lru_cache
from transformers import pipeline


@lru_cache(maxsize=1)
def get_classifier():
    return pipeline("text-classification", model="ProsusAI/finbert", tokenizer="ProsusAI/finbert")


def analyze_sentiment(text: str, max_sentences: int = 200) -> dict:
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) >= 20]
    sentences = sentences[:max_sentences]
    if not sentences:
        return {"label": "neutral", "score": 0.0, "positive": 0.0, "negative": 0.0, "neutral": 1.0, "sentences": 0}

    classifier = get_classifier()
    predictions = classifier(sentences, truncation=True, max_length=512)
    weighted = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
    for prediction in predictions:
        weighted[prediction["label"]] += float(prediction["score"])

    n = len(predictions)
    averages = {key: value / n for key, value in weighted.items()}
    label = max(averages, key=averages.get)
    return {
        "label": label,
        "score": round(averages[label], 4),
        "positive": round(averages["positive"], 4),
        "negative": round(averages["negative"], 4),
        "neutral": round(averages["neutral"], 4),
        "sentences": n,
    }
