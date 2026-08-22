from nlp.keywords import keyword_frequency


def test_keyword_frequency():
    result = keyword_frequency("AI AI inflation capex expansion risk")
    assert result["AI"] == 2
    assert result["Inflation"] == 1
    assert result["CapEx"] == 1
    assert result["Expansion"] == 1
    assert result["Risk"] == 1
