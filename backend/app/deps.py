from sqlmodel import Session

from .db import get_session


def get_db() -> Session:
    db = get_session()
    try:
        yield db
    finally:
        db.close()

