LEGAL EASE QUICK START

1) Open LegalEase in VS Code.
2) python -m venv .venv
3) Activate .venv.
4) pip install -r requirements.txt
5) Copy .env.example to .env and add GEMINI_API_KEY.
6) Backend: uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
7) Frontend: streamlit run app.py
8) Test: pytest -q

For UI testing without Gemini, set DEMO_MODE=true in .env.
