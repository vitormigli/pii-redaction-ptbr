from pii_redaction.patterns import find_structured_pii


def test_finds_cpf():
    spans = find_structured_pii("O CPF é 123.456.789-09.")
    assert any(s.label == "CPF" and s.text == "123.456.789-09" for s in spans)


def test_finds_cnpj():
    spans = find_structured_pii("CNPJ: 12.345.678/0001-95")
    assert any(s.label == "CNPJ" and s.text == "12.345.678/0001-95" for s in spans)


def test_finds_email():
    spans = find_structured_pii("Contato: fulano@example.com")
    assert any(s.label == "EMAIL" and s.text == "fulano@example.com" for s in spans)


def test_finds_phone():
    spans = find_structured_pii("Ligue (11) 98765-4321 por favor.")
    assert any(s.label == "TELEFONE" for s in spans)


def test_finds_cep():
    spans = find_structured_pii("CEP 01310-100")
    assert any(s.label == "CEP" and s.text == "01310-100" for s in spans)


def test_cnpj_not_double_counted_as_cpf():
    spans = find_structured_pii("CNPJ: 12.345.678/0001-95")
    labels = [s.label for s in spans]
    assert labels.count("CPF") == 0


def test_no_false_positive_on_plain_sentence():
    spans = find_structured_pii("Essa frase não tem nenhum dado pessoal.")
    assert spans == []
