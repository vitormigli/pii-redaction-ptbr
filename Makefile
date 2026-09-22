.PHONY: run demo eval test lint

run:
	uv run uvicorn pii_redaction.api:app --host 0.0.0.0 --port 8000 --reload

demo:
	uv run streamlit run src/pii_redaction/streamlit_app.py

eval:
	uv run python evals/run_eval.py

test:
	uv run pytest

lint:
	uv run ruff check .
