from __future__ import annotations


def extract_entities(text: str) -> list[dict[str, str]]:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError as exc:
        raise RuntimeError("Install the spaCy model with: python -m spacy download en_core_web_sm") from exc
    doc = nlp(text[:100000])
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
