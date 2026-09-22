"""Combines structured-PII regex detection and NER person-name detection into
one redaction pass, with consistent per-entity placeholder numbering."""

from pii_redaction.ner import find_person_names, load_ner_model
from pii_redaction.patterns import Span, find_structured_pii


def _merge_overlaps(spans: list[Span]) -> list[Span]:
    """When a structured pattern and a NER span overlap, keep the structured
    one (regex detectors here are more precise than generic NER)."""
    spans = sorted(spans, key=lambda s: (s.start, -(s.end - s.start)))
    merged: list[Span] = []
    last_end = -1
    for span in spans:
        if span.start >= last_end:
            merged.append(span)
            last_end = span.end
    return merged


def detect(text: str, nlp=None) -> list[Span]:
    structured = find_structured_pii(text)
    names = find_person_names(nlp or load_ner_model(), text)
    return _merge_overlaps(structured + names)


def redact(text: str, nlp=None) -> tuple[str, list[Span]]:
    spans = detect(text, nlp)
    placeholder_by_text: dict[tuple[str, str], str] = {}
    counters: dict[str, int] = {}

    result = []
    cursor = 0
    for span in spans:
        result.append(text[cursor:span.start])
        key = (span.label, span.text.lower())
        if key not in placeholder_by_text:
            counters[span.label] = counters.get(span.label, 0) + 1
            placeholder_by_text[key] = f"[{span.label}_{counters[span.label]}]"
        result.append(placeholder_by_text[key])
        cursor = span.end
    result.append(text[cursor:])

    return "".join(result), spans
