from fastapi.testclient import TestClient

from app.main import app


c = TestClient(app)


def test_analyze():
    r = c.post("/analyze", json={"text": "I feel overwhelmed by study deadlines"})
    assert r.status_code == 200
    j = r.json()
    assert "emotion" in j and "plan" in j


def test_feedback():
    j = c.post("/analyze", json={"text": "I argue with my friend a lot"}).json()
    r = c.post("/feedback", json={"inference_id": j["inference_id"], "helpful": 1})
    assert r.status_code == 200

