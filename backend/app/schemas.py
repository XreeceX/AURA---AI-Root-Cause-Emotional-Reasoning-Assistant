from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    text: str = Field(min_length=1)


class AnalyzeResponse(BaseModel):
    session_id: int
    inference_id: int
    emotion: str
    sentiment: str
    distortions: List[str]
    facets: List[str]
    causes: List[str]
    plan: Dict[str, Any]


class FeedbackRequest(BaseModel):
    inference_id: int
    helpful: int = Field(ge=-1, le=1)
    notes: Optional[str] = None


class ProfileDelta(BaseModel):
    user_id: int
    deltas: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class ProfileOut(BaseModel):
    user_id: int
    emotion_weights: Dict[str, float]
    distortion_weights: Dict[str, float]
    coping_prefs: Dict[str, Any]

