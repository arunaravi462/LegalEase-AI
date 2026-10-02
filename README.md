# LegalEase — AI-Powered Legal Document Generator

Complete implementation based on the supplied LegalEase specification: Streamlit frontend, FastAPI backend, Gemini integration, editable preview, and TXT/DOCX/PDF export. fileciteturn0file0L113-L141

## Setup
1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create a virtual environment: `python -m venv .venv`.
4. Activate it, then run `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
6. Keep `GEMINI_MODEL=gemini-1.5-pro` to match the supplied specification, or change it to a model available to your Google API account.
7. For local UI testing without an API key, set `DEMO_MODE=true`.

## Run
Terminal 1: `uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000`

Terminal 2: `streamlit run app.py`

FastAPI docs: http://127.0.0.1:8000/docs
Streamlit: http://localhost:8501

## Test
With the virtual environment active: `pytest -q`

## Features
- document type, parties, terms and effective date input
- Gemini-backed draft generation
- editable preview
- TXT, DOCX and PDF export
- logo/header/footer branding
- FastAPI validation and error handling
- demo mode for offline UI testing
- automated tests

The source specification explicitly requires the `/generate` FastAPI endpoint and these input fields, plus TXT/DOCX/PDF output. fileciteturn0file0L44-L52

> LegalEase produces AI-assisted drafts and general information, not legal advice. Have appropriate legal counsel review documents before use.
