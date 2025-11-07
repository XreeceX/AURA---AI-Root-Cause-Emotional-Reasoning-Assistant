# AURA MVP

AURA (AI Root-Cause & Emotional Reasoning Assistant) runs locally with a FastAPI backend, lightweight NLP pipelines, and a minimal HTML frontend.

## Features
- Analyze free-text reflections into emotion, sentiment, facets, cognitive distortions, hypothesized causes, and a 7-day action plan
- Capture user feedback to adapt personal profiles via bandit-style weight updates
- Persist users, sessions, messages, inferences, feedback, and profiles in SQLite
- Offline-friendly: Hugging Face pipelines load locally; no external services required

## Quickstart

**One command (works on Windows, Mac, Linux):**
```bash
python run.py
```

On Unix systems, you can also make it executable:
```bash
chmod +x run.py
./run.py
```

This will:
- Check Python 3.10+ is installed
- Create a virtual environment
- Install all dependencies
- Start the server on http://localhost:8000
- Open the frontend in your browser

**Alternative (manual setup):**
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Then open `frontend/index.html` in your browser.

## API
- `POST /analyze` `{text, user_id?, session_id?}` → inference payload
- `POST /feedback` `{inference_id, helpful, notes?}` → feedback receipt + profile snapshot
- `GET /profile/{user_id}` → current profile weights
- `POST /profile/tune` `{user_id, deltas}` → manual profile adjustments

## Docker
```bash
docker build -t aura .
docker run -p 8000:8000 aura
```

## Safety Notes
- Not therapy or medical care. Displayed warnings remind users to seek professional help for crises.
- Data stays on-device. Clearing the browser cache removes UI-side session traces.

