"""A tiny fake NER model exposing spaCy's `.ents` interface, so tests never
need to download real model weights."""

from dataclasses import dataclass

import pytest


@dataclass
class FakeEnt:
    text: str
    label_: str
    start_char: int
    end_char: int


class FakeDoc:
    def __init__(self, ents: list[FakeEnt]):
        self.ents = ents


class FakeNER:
    """Recognizes any two-capitalized-word sequence as a PER entity —
    good enough to exercise the merge/placeholder logic in tests."""

    def __call__(self, text: str):
        import re

        ents = []
        for match in re.finditer(r"\b[A-ZÀ-Ú][a-zà-ú]+ [A-ZÀ-Ú][a-zà-ú]+\b", text):
            ents.append(
                FakeEnt(
                    text=match.group(), label_="PER", start_char=match.start(), end_char=match.end()
                )
            )
        return FakeDoc(ents)


@pytest.fixture
def fake_ner():
    return FakeNER()
