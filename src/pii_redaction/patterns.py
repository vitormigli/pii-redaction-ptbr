"""Regex detectors for structured PII in Brazilian Portuguese text. Deliberately
favors recall over precision — see docs/decisions/0001-favor-recall.md."""

import re
from dataclasses import dataclass


@dataclass
class Span:
    label: str
    start: int
    end: int
    text: str


_PATTERNS: dict[str, re.Pattern] = {
    "CPF": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b"),
    "CNPJ": re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "TELEFONE": re.compile(
        r"(?:\+55\s?)?\(?\d{2}\)?\s?9?\d{4}-?\d{4}\b"
    ),
    "CEP": re.compile(r"\b\d{5}-\d{3}\b"),
}

# CPF's plain-11-digit pattern is checked last and only applied where no other
# pattern already claimed the span, to avoid CPF swallowing part of a CNPJ or a
# formatted phone number that also happens to have 11 digits somewhere.
_ORDERED_LABELS = ["CNPJ", "EMAIL", "CEP", "TELEFONE", "CPF"]


def find_structured_pii(text: str) -> list[Span]:
    spans: list[Span] = []
    claimed = [False] * len(text)

    for label in _ORDERED_LABELS:
        for match in _PATTERNS[label].finditer(text):
            start, end = match.span()
            if any(claimed[start:end]):
                continue
            spans.append(Span(label=label, start=start, end=end, text=match.group()))
            for i in range(start, end):
                claimed[i] = True

    return sorted(spans, key=lambda s: s.start)
