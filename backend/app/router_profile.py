from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .deps import get_db
from .models import Profile
from .profile import get_or_create_profile
from .schemas import ProfileDelta, ProfileOut


router = APIRouter()


@router.get("/profile/{user_id}", response_model=ProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    p = get_or_create_profile(db, user_id)
    return {
        "user_id": user_id,
        "emotion_weights": p.emotion_weights,
        "distortion_weights": p.distortion_weights,
        "coping_prefs": p.coping_prefs,
    }


@router.post("/profile/tune")
def tune_profile(delta: ProfileDelta, db: Session = Depends(get_db)):
    p = get_or_create_profile(db, delta.user_id)
    ew = p.emotion_weights
    dw = p.distortion_weights
    cp = p.coping_prefs
    for k, v in delta.deltas.get("emotion_weights", {}).items():
        ew[k] = ew.get(k, 0) + v
    for k, v in delta.deltas.get("distortion_weights", {}).items():
        dw[k] = dw.get(k, 0) + v
    for k, v in delta.deltas.get("coping_prefs", {}).items():
        cp[k] = v
    p.emotion_weights, p.distortion_weights, p.coping_prefs = ew, dw, cp
    p.last_updated = datetime.now(timezone.utc)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"ok": True}

