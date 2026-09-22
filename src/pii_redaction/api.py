"""FastAPI service exposing POST /redact."""

from fastapi import FastAPI
from pydantic import BaseModel

from pii_redaction.redactor import redact

app = FastAPI(title="PII Redaction (pt-BR)")


class RedactRequest(BaseModel):
    text: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/redact")
def redact_endpoint(req: RedactRequest) -> dict:
    redacted_text, spans = redact(req.text)
    return {
        "redacted_text": redacted_text,
        "entities": [
            {"label": s.label, "text": s.text, "start": s.start, "end": s.end} for s in spans
        ],
    }
