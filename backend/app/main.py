from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .router_analysis import router as analysis_router
from .router_feedback import router as feedback_router
from .router_profile import router as profile_router


app = FastAPI(title="AURA")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(analysis_router)
app.include_router(feedback_router)
app.include_router(profile_router)


@app.on_event("startup")
def startup():
    init_db()

