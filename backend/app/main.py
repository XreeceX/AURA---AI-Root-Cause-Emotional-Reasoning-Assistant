from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/health")
def health():
    """Quick health check - returns before models load."""
    return {"status": "ok"}

