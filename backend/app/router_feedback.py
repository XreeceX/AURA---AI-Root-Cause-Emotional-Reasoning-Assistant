from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from .deps import get_db
from .models import Feedback, Inference, SessionModel
from .profile import get_or_create_profile, update_profile_from_feedback
from .schemas import FeedbackRequest


router = APIRouter()


@router.post("/feedback")
def feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    inf = db.get(Inference, req.inference_id)
    if not inf:
        raise HTTPException(status_code=404, detail="Inference not found")
    fb = Feedback(inference_id=inf.id, helpful=req.helpful, notes=req.notes)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    s = db.get(SessionModel, inf.session_id)
    if not s or s.user_id is None:
        return {"feedback_id": fb.id, "profile": None}
    p = get_or_create_profile(db, s.user_id)
    p = update_profile_from_feedback(db, p, inf, req.helpful)
    return {"feedback_id": fb.id, "profile": {"emotion_weights": p.emotion_weights, "distortion_weights": p.distortion_weights}}

