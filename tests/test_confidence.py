from nlp.confidence import calculate_confidence


def test_confidence_stays_in_range():
    sentiment = {"positive": 0.9, "negative": 0.05}
    keywords = {"Expansion": 20, "CapEx": 20, "AI": 20, "Inflation": 1, "Risk": 1}
    score = calculate_confidence(sentiment, keywords)
    assert 0 <= score <= 100


def test_risk_lowers_confidence():
    sentiment = {"positive": 0.7, "negative": 0.1}
    low_risk = {"Expansion": 5, "CapEx": 5, "AI": 5, "Inflation": 0, "Risk": 0}
    high_risk = {"Expansion": 5, "CapEx": 5, "AI": 5, "Inflation": 0, "Risk": 20}
    assert calculate_confidence(sentiment, high_risk) < calculate_confidence(sentiment, low_risk)
