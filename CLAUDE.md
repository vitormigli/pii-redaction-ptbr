# Project instructions for Claude

This project follows the rules of the portfolio master plan:

1. No client code or data — synthetic sentences only (see `evals/dataset.py`).
2. No committed secrets — this project needs none (no paid API is called;
   `gitleaks` still runs on pre-commit and in CI as a safety net).
3. Every project reports numeric evaluation metrics — see `evals/results.md`.
4. Everything runs with a single command: `docker compose up` or `make run`.
5. README in English, with a short "Resumo em português" section at the end.
   Header banner + badges matching the other portfolio repos.
6. Small, descriptive commits using Conventional Commits.
7. Prefer simplicity — regex for structured PII, spaCy directly for names, no
   heavier PII-detection framework.

## Layout

- `src/pii_redaction/patterns.py` — regex detectors (CPF, CNPJ, email, phone, CEP).
- `src/pii_redaction/ner.py` — spaCy-based person-name detection.
- `src/pii_redaction/redactor.py` — merges both, produces redacted text with
  consistent per-entity placeholders.
- `evals/run_eval.py` — precision/recall/F1 per entity type against
  `evals/dataset.py`'s gold annotations; the only network call this project ever
  makes is downloading the spaCy model once, and it's free.
