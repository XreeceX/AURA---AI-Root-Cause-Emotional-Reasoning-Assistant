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
- `GET /health` → quick health check (responds before models load)
- `POST /analyze` `{text, user_id?, session_id?}` → inference payload
- `POST /feedback` `{inference_id, helpful, notes?}` → feedback receipt + profile snapshot
- `GET /profile/{user_id}` → current profile weights
- `POST /profile/tune` `{user_id, deltas}` → manual profile adjustments

**Note:** NLP models load lazily on the first `/analyze` request, so server startup is fast. The first analysis may take 30–60 seconds.

## Docker
```bash
docker build -t aura .
docker run -p 8000:8000 aura
```

## Deploy on Vercel

This repo is configured for Vercel with:
- `api/index.py` as the Python serverless entrypoint
- `vercel.json` routes (`/api/*` to backend, all other routes to frontend)

### Steps
1. Import this repo into Vercel
2. Framework preset: **Other**
3. Root directory: project root
4. Deploy

### Notes on "24/7"
- Vercel serverless functions are **not always-on processes**. They spin up on request and may cold-start.
- The serverless file system is ephemeral; SQLite is configured to use `/tmp/aura.db` on Vercel runtime.
- For true persistent always-on backend + durable database, deploy backend on a long-running host (e.g. Railway/Render/Fly) and use Vercel for frontend.

## Safety Notes
- Not therapy or medical care. Displayed warnings remind users to seek professional help for crises.
- Data stays on-device. Clearing the browser cache removes UI-side session traces.

