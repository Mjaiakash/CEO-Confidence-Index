from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from config import FINBERT_MODEL
from preprocessing.clean_text import split_sentences


@dataclass(frozen=True)
class SentimentResult:
    positive: float
    negative: float
    neutral: float
    polarity: float
    sentences_analyzed: int


@lru_cache(maxsize=1)
def _classifier():
    from transformers import pipeline
    return pipeline("text-classification", model=FINBERT_MODEL, tokenizer=FINBERT_MODEL, truncation=True, max_length=512)


def analyze_sentiment(text: str, max_sentences: int = 250) -> SentimentResult:
    sentences = split_sentences(text)[:max_sentences]
    if not sentences:
        return SentimentResult(0.0, 0.0, 0.0, 0.0, 0)
    outputs = _classifier()(sentences, batch_size=8)
    positive = [item["score"] for item in outputs if item["label"].lower() == "positive"]
    negative = [item["score"] for item in outputs if item["label"].lower() == "negative"]
    neutral = [item["score"] for item in outputs if item["label"].lower() == "neutral"]
    p = float(np.mean(positive)) if positive else 0.0
    n = float(np.mean(negative)) if negative else 0.0
    z = float(np.mean(neutral)) if neutral else 0.0
    return SentimentResult(p, n, z, p - n, len(sentences))
