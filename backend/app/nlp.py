from transformers import pipeline


class NLP:
    def __init__(self, sentiment_model, zero_shot_model):
        self.sentiment = pipeline("sentiment-analysis", model=sentiment_model)
        self.zs = pipeline("zero-shot-classification", model=zero_shot_model, multi_label=True)
        self.emotions = ["joy", "sadness", "anger", "fear", "anxiety", "frustration", "guilt", "shame", "loneliness", "overwhelm"]
        self.facets = ["work", "study", "family", "relationship", "health", "money", "sleep", "time-management", "motivation", "confidence", "social", "focus"]
        self.distortions = ["catastrophizing", "overgeneralization", "personalization", "mind-reading", "all-or-nothing", "should-statements", "fortune-telling", "filtering"]

    def analyze(self, text, topk=3):
        s = self.sentiment(text)[0]["label"].lower()
        e = self.zs(text, self.emotions)
        f = self.zs(text, self.facets)
        d = self.zs(text, self.distortions)
        emo = e["labels"][:topk]
        facets = f["labels"][:topk]
        dists = d["labels"][:topk]
        emotion = emo[0] if emo else "neutral"
        return s, emotion, facets, dists

