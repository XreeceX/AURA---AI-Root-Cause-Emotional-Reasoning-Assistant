from datetime import datetime, timezone
from typing import Any

from sqlmodel import select
from sqlmodel import Session

from .models import Profile


def _save_and_refresh(db: Session, instance: Any) -> None:
    db.add(instance)
    db.commit()
    db.refresh(instance)


def get_or_create_profile(db: Session, user_id: int) -> Profile:
    profile = db.exec(select(Profile).where(Profile.user_id == user_id)).first()
    if profile:
        return profile
    profile = Profile(user_id=user_id, emotion_weights={}, distortion_weights={}, coping_prefs={})
    _save_and_refresh(db, profile)
    return profile


def update_profile_from_feedback(db: Session, profile: Profile, inference, helpful: int) -> Profile:
    ew = profile.emotion_weights
    dw = profile.distortion_weights
    for e in [inference.emotion]:
        ew[e] = ew.get(e, 0) + (1 if helpful > 0 else -0.5)
    for d in inference.distortions:
        dw[d] = dw.get(d, 0) + (0.5 if helpful > 0 else -0.25)
    profile.emotion_weights = ew
    profile.distortion_weights = dw
    profile.last_updated = datetime.now(timezone.utc)
    _save_and_refresh(db, profile)
    return profile

