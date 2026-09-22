# 1. Favor recall over precision for structured PII

## Status

Accepted

## Context

This tool exists to keep PII out of text before it's sent somewhere it shouldn't be
(logs, prompts to third-party APIs, etc.). A missed CPF is a compliance/privacy
incident; a false positive is a slightly-over-redacted sentence — the two failure
modes are not equally bad.

## Decision

Structured-PII regex patterns (CPF, CNPJ, phone) match on shape alone — no check-digit
validation gates whether something gets redacted. A number that merely looks like a
CPF gets masked, even if its check digits are actually invalid.

## Consequences

- Higher recall, lower precision on structured entities than a checksum-gated
  detector would have — visible in `evals/results.md`.
- Safe default for a redaction tool. A checksum-validated variant would be the right
  choice for a different use case (e.g. deciding whether to *trust* a CPF as real,
  as `doc-extraction-pipeline` does) — redaction and validation are different jobs
  even though they share a regex.
