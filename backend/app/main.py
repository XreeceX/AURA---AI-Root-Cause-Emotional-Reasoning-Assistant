from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .db import init_db
from .router_analysis import router as analysis_router
from .router_feedback import router as feedback_router
from .router_profile import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Cleanup if needed


app = FastAPI(
    title="AURA",
    description="AI Root-Cause & Emotional Reasoning Assistant",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analysis_router)
app.include_router(feedback_router)
app.include_router(profile_router)
# Also expose API routes under /api for hosted environments.
app.include_router(analysis_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")
app.include_router(profile_router, prefix="/api")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_INDEX = FRONTEND_DIR / "index.html"
FRONTEND_CSS = FRONTEND_DIR / "aura.css"
FRONTEND_JS = FRONTEND_DIR / "aura.js"


@app.get("/", include_in_schema=False)
def home():
    if FRONTEND_INDEX.exists():
        return FileResponse(FRONTEND_INDEX)
    return {"status": "ok"}


@app.get("/aura.css", include_in_schema=False)
def frontend_css():
    if FRONTEND_CSS.exists():
        return FileResponse(FRONTEND_CSS, media_type="text/css")
    return {"detail": "Not found"}


@app.get("/aura.js", include_in_schema=False)
def frontend_js():
    if FRONTEND_JS.exists():
        return FileResponse(FRONTEND_JS, media_type="application/javascript")
    return {"detail": "Not found"}


@app.get("/health")
def health():
    """Quick health check - returns before models load."""
    return {"status": "ok"}


@app.get("/api/health")
def api_health():
    return {"status": "ok"}

