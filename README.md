# ChefGenie API (Backend)

RAG + LLM backend to suggest recipes from your pantry, with allergy/diet filters and optional image-based ingredient extraction.

## Quick Start

```bash
cp .env.example .env
# put your OPENAI_API_KEY in .env (or Azure OpenAI vars)

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Ingest KB
python ingest_kb.py

# Run API
uvicorn app.main:app --reload