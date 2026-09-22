FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --no-install-project || true

COPY . .
RUN uv sync
RUN uv run python -m spacy download pt_core_news_sm

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "pii_redaction.api:app", "--host", "0.0.0.0", "--port", "8000"]
