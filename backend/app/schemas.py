from typing import Dict, List, Optional

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    text: str


class AnalyzeResponse(BaseModel):
    session_id: int
    inference_id: int
    emotion: str
    sentiment: str
    distortions: List[str]
    facets: List[str]
    causes: List[str]
    plan: Dict


class FeedbackRequest(BaseModel):
    inference_id: int
    helpful: int
    notes: Optional[str] = None


class ProfileDelta(BaseModel):
    user_id: int
    deltas: Dict


class ProfileOut(BaseModel):
    user_id: int
    emotion_weights: Dict
    distortion_weights: Dict
    coping_prefs: Dict

