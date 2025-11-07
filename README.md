# AURA MVP

AURA (AI Root-Cause & Emotional Reasoning Assistant) runs locally with a FastAPI backend, lightweight NLP pipelines, and a minimal HTML frontend.

## Features
- Analyze free-text reflections into emotion, sentiment, facets, cognitive distortions, hypothesized causes, and a 7-day action plan
- Capture user feedback to adapt personal profiles via bandit-style weight updates
- Persist users, sessions, messages, inferences, feedback, and profiles in SQLite
- Offline-friendly: Hugging Face pipelines load locally; no external services required

## Quickstart
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend/app --reload
```
Open `frontend/index.html` in a browser (CORS enabled for localhost).

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

