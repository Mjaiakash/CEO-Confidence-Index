from nlp.confidence import confidence_score
from nlp.keywords import keyword_frequency
from preprocessing.clean_text import clean_text, split_sentences


def test_clean_text():
    assert clean_text("Hello   world") == "Hello world"


def test_split_sentences():
    assert split_sentences("One. Two!") == ["One.", "Two!"]


def test_keyword_frequency():
    result = keyword_frequency("AI AI inflation capex expansion risk")
    assert result["AI"] == 2
    assert result["Inflation"] == 1
    assert result["CapEx"] == 1
    assert result["Expansion"] == 1
    assert result["Risk"] == 1


def test_confidence_bounds():
    score = confidence_score(1.0, {"AI": 100, "Inflation": 0, "Expansion": 40, "CapEx": 40, "Risk": 0})
    assert 0 <= score <= 100
