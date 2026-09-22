from pii_redaction.redactor import detect, redact


def test_redact_masks_cpf_and_email(fake_ner):
    text = "Meu CPF é 123.456.789-09 e meu email é a@b.com."
    redacted, spans = redact(text, nlp=fake_ner)
    assert "123.456.789-09" not in redacted
    assert "a@b.com" not in redacted
    assert "[CPF_1]" in redacted
    assert "[EMAIL_1]" in redacted


def test_redact_gives_same_placeholder_to_repeated_entity(fake_ner):
    text = "Carla Mendes ligou. Depois, Carla Mendes ligou de novo."
    redacted, spans = redact(text, nlp=fake_ner)
    assert redacted.count("[PESSOA_1]") == 2
    assert "[PESSOA_2]" not in redacted


def test_redact_gives_different_placeholders_to_different_entities(fake_ner):
    text = "Carla Mendes e João Silva participaram da reunião."
    redacted, spans = redact(text, nlp=fake_ner)
    assert "[PESSOA_1]" in redacted
    assert "[PESSOA_2]" in redacted


def test_detect_merges_overlapping_structured_and_ner_spans(fake_ner):
    # A CPF-shaped number should never also get swallowed by a name-shaped NER match.
    text = "Ana Costa, CPF 123.456.789-09."
    spans = detect(text, nlp=fake_ner)
    labels = {s.label for s in spans}
    assert "CPF" in labels
    assert "PESSOA" in labels


def test_redact_leaves_plain_text_untouched(fake_ner):
    text = "Nenhum dado pessoal nesta frase."
    redacted, spans = redact(text, nlp=fake_ner)
    assert redacted == text
    assert spans == []
