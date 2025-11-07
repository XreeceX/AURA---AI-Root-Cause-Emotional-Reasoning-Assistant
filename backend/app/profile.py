from datetime import datetime

from .models import Profile


def get_or_create_profile(db, user_id):
    p = db.query(Profile).where(Profile.user_id == user_id).first()
    if p:
        return p
    p = Profile(user_id=user_id, emotion_weights={}, distortion_weights={}, coping_prefs={})
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def update_profile_from_feedback(db, profile: Profile, inference, helpful: int):
    ew = profile.emotion_weights
    dw = profile.distortion_weights
    for e in [inference.emotion]:
        ew[e] = ew.get(e, 0) + (1 if helpful > 0 else -0.5)
    for d in inference.distortions:
        dw[d] = dw.get(d, 0) + (0.5 if helpful > 0 else -0.25)
    profile.emotion_weights = ew
    profile.distortion_weights = dw
    profile.last_updated = datetime.utcnow()
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

