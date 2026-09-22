"""Wraps a spaCy Portuguese NER model to find person names. Pass a pre-loaded
`nlp` (or any object exposing spaCy's `nlp(text).ents` interface) to avoid
downloading model weights in tests."""

from functools import lru_cache

from pii_redaction.patterns import Span

SPACY_MODEL_NAME = "pt_core_news_sm"


@lru_cache(maxsize=1)
def load_ner_model():
    import spacy

    return spacy.load(SPACY_MODEL_NAME)


def find_person_names(nlp, text: str) -> list[Span]:
    doc = nlp(text)
    return [
        Span(label="PESSOA", start=ent.start_char, end=ent.end_char, text=ent.text)
        for ent in doc.ents
        if ent.label_ == "PER"
    ]
