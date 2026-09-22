"""Synthetic pt-BR sentences containing PII, with gold entity annotations.
All names, numbers and documents are fabricated for this eval."""

EXAMPLES: list[dict] = [
    {
        "text": "Meu nome é Carla Mendes, CPF 123.456.789-09, e meu e-mail é carla.mendes@example.com.",  # noqa: E501
        "gold": [
            ("PESSOA", "Carla Mendes"),
            ("CPF", "123.456.789-09"),
            ("EMAIL", "carla.mendes@example.com"),
        ],
    },
    {
        "text": "O contrato foi assinado por João Pereira, telefone (11) 98765-4321.",
        "gold": [("PESSOA", "João Pereira"), ("TELEFONE", "(11) 98765-4321")],
    },
    {
        "text": "A empresa Acme Ltda, CNPJ 12.345.678/0001-95, faturou o pedido.",
        "gold": [("CNPJ", "12.345.678/0001-95")],
    },
    {
        "text": "Envie a correspondência para o CEP 01310-100, aos cuidados de Beatriz Alves.",
        "gold": [("CEP", "01310-100"), ("PESSOA", "Beatriz Alves")],
    },
    {
        "text": "Para dúvidas, contate suporte@empresa.com.br ou ligue (21) 3333-4444.",
        "gold": [("EMAIL", "suporte@empresa.com.br"), ("TELEFONE", "(21) 3333-4444")],
    },
    {
        "text": "Ricardo Souza confirmou o cadastro com o CPF 987.654.321-00.",
        "gold": [("PESSOA", "Ricardo Souza"), ("CPF", "987.654.321-00")],
    },
    {
        "text": "A reunião com Fernanda Lima foi remarcada para sexta-feira.",
        "gold": [("PESSOA", "Fernanda Lima")],
    },
    {
        "text": "O e-mail antigo, contato@antiga.com, não deve mais ser usado por Paulo Rocha.",
        "gold": [("EMAIL", "contato@antiga.com"), ("PESSOA", "Paulo Rocha")],
    },
    {
        "text": "Segue o CNPJ da filial: 98.765.432/0001-10, cadastrado por Camila Santos.",
        "gold": [("CNPJ", "98.765.432/0001-10"), ("PESSOA", "Camila Santos")],
    },
    {
        "text": "Nenhum dado pessoal aparece nesta frase de controle.",
        "gold": [],
    },
    {
        "text": "Lucas Tavares mora perto do CEP 04567-000 e pode ser contatado em lucas.t@mail.com.",  # noqa: E501
        "gold": [("PESSOA", "Lucas Tavares"), ("CEP", "04567-000"), ("EMAIL", "lucas.t@mail.com")],
    },
    {
        "text": "O CPF 111.222.333-44 pertence a Mariana Costa, telefone 11987654321.",
        "gold": [
            ("CPF", "111.222.333-44"),
            ("PESSOA", "Mariana Costa"),
            ("TELEFONE", "11987654321"),
        ],
    },
]
