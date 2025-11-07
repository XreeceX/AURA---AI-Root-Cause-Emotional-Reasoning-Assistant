from fastapi import APIRouter, Depends
from sqlmodel import Session

from .deps import get_db
from .models import Inference, Message, SessionModel, User
from .nlp import NLP
from .planning import plan_7day
from .reasoning import hypothesize_causes
from .schemas import AnalyzeRequest, AnalyzeResponse
from .settings import settings


router = APIRouter()
nlp = NLP(settings.sentiment_model, settings.zero_shot_model)


def get_or_create_user(db: Session, user_id=None):
    if user_id:
        u = db.get(User, user_id)
        if u:
            return u
    u = User()
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def get_or_create_session(db: Session, user_id, session_id=None):
    if session_id:
        s = db.get(SessionModel, session_id)
        if s:
            return s
    s = SessionModel(user_id=user_id)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    u = get_or_create_user(db, req.user_id)
    s = get_or_create_session(db, u.id, req.session_id)
    m = Message(session_id=s.id, role="user", text=req.text)
    db.add(m)
    db.commit()
    sentiment, emotion, facets, dists = nlp.analyze(req.text, topk=settings.topk)
    causes = hypothesize_causes(sentiment, emotion, facets, dists)
    plan = plan_7day(emotion, facets, dists, causes)
    inf = Inference(session_id=s.id, emotion=emotion, sentiment=sentiment, distortions=dists, facets=facets, causes=causes, plan=plan, score=0.0)
    db.add(inf)
    db.commit()
    db.refresh(inf)
    return {
        "session_id": s.id,
        "inference_id": inf.id,
        "emotion": emotion,
        "sentiment": sentiment,
        "distortions": dists,
        "facets": facets,
        "causes": causes,
        "plan": plan,
    }

