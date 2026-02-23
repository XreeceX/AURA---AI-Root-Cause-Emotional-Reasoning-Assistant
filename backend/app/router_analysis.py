from typing import Optional

from fastapi import APIRouter, Depends
from sqlmodel import Session

from .deps import get_db
from .models import Inference, Message, SessionModel, User
from .nlp import get_nlp
from .planning import plan_7day
from .reasoning import hypothesize_causes
from .schemas import AnalyzeRequest, AnalyzeResponse
from .settings import settings


router = APIRouter()


def _nlp():
    return get_nlp(settings.sentiment_model, settings.zero_shot_model)


def _save_and_refresh(db: Session, instance) -> None:
    db.add(instance)
    db.commit()
    db.refresh(instance)


def get_or_create_user(db: Session, user_id: Optional[int] = None) -> User:
    if user_id:
        user = db.get(User, user_id)
        if user:
            return user
    user = User()
    _save_and_refresh(db, user)
    return user


def get_or_create_session(db: Session, user_id: int, session_id: Optional[int] = None) -> SessionModel:
    if session_id:
        session = db.get(SessionModel, session_id)
        if session:
            return session
    session = SessionModel(user_id=user_id)
    _save_and_refresh(db, session)
    return session


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    user = get_or_create_user(db, req.user_id)
    session = get_or_create_session(db, user.id, req.session_id)
    message = Message(session_id=session.id, role="user", text=req.text)
    _save_and_refresh(db, message)

    nlp = _nlp()
    sentiment, emotion, facets, dists = nlp.analyze(req.text, topk=settings.topk)
    causes = hypothesize_causes(sentiment, emotion, facets, dists)
    plan = plan_7day(emotion, facets, dists, causes)
    inf = Inference(
        session_id=session.id,
        emotion=emotion,
        sentiment=sentiment,
        distortions=dists,
        facets=facets,
        causes=causes,
        plan=plan,
        score=0.0,
    )
    _save_and_refresh(db, inf)
    return {
        "session_id": session.id,
        "inference_id": inf.id,
        "emotion": emotion,
        "sentiment": sentiment,
        "distortions": dists,
        "facets": facets,
        "causes": causes,
        "plan": plan,
    }

