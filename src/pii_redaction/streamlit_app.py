"""Streamlit demo: paste text, see it redacted and the detected entities."""

import streamlit as st

from pii_redaction.redactor import redact

st.set_page_config(page_title="PII Redaction (pt-BR)", page_icon="🔒")
st.title("PII Redaction (pt-BR)")
st.caption("Detecta e mascara CPF, CNPJ, e-mail, telefone, CEP e nomes de pessoas — 100% local.")

default_text = (
    "Meu nome é Carla Mendes, CPF 123.456.789-09, e meu e-mail é carla.mendes@example.com. "
    "Pode ligar no (11) 98765-4321."
)
text = st.text_area("Texto de entrada", value=default_text, height=150)

if st.button("Redigir"):
    redacted_text, spans = redact(text)
    st.subheader("Texto redigido")
    st.write(redacted_text)
    st.subheader("Entidades detectadas")
    st.json([{"label": s.label, "text": s.text} for s in spans])
