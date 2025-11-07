from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    handle: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="sessionmodel.id")
    role: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Inference(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="sessionmodel.id")
    emotion: str
    sentiment: str
    distortions: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    facets: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    causes: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    plan: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    inference_id: int = Field(foreign_key="inference.id")
    helpful: int
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    emotion_weights: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    distortion_weights: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    coping_prefs: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    last_updated: datetime = Field(default_factory=datetime.utcnow)

