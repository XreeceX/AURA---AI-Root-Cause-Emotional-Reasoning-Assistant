from transformers import pipeline

_nlp_instance = None


def get_nlp(sentiment_model: str, zero_shot_model: str) -> "NLP":
    """Lazy-loaded singleton. Models load on first analyze request, not at server startup."""
    global _nlp_instance
    if _nlp_instance is None:
        _nlp_instance = NLP(sentiment_model, zero_shot_model)
    return _nlp_instance


class NLP:
    def __init__(self, sentiment_model: str, zero_shot_model: str):
        self.sentiment = pipeline("sentiment-analysis", model=sentiment_model)
        self.zs = pipeline("zero-shot-classification", model=zero_shot_model, multi_label=True)
        self.emotions = [
            "joy", "sadness", "anger", "fear", "anxiety", "frustration",
            "guilt", "shame", "loneliness", "overwhelm",
        ]
        self.facets = [
            "work", "study", "family", "relationship", "health", "money",
            "sleep", "time-management", "motivation", "confidence", "social", "focus",
        ]
        self.distortions = [
            "catastrophizing", "overgeneralization", "personalization", "mind-reading",
            "all-or-nothing", "should-statements", "fortune-telling", "filtering",
        ]

    def analyze(self, text: str, topk: int = 3):
        s = self.sentiment(text[:512])[0]["label"].lower()
        e = self.zs(text[:512], self.emotions)
        f = self.zs(text[:512], self.facets)
        d = self.zs(text[:512], self.distortions)
        emo = e["labels"][:topk]
        facets = f["labels"][:topk]
        dists = d["labels"][:topk]
        emotion = emo[0] if emo else "neutral"
        return s, emotion, facets, dists

