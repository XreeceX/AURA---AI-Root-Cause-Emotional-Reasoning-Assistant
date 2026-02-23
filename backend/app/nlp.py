from __future__ import annotations

from typing import List, Sequence, Tuple

try:
    from transformers import pipeline  # type: ignore
except Exception:  # pragma: no cover - optional dependency in serverless mode
    pipeline = None

_nlp_instance = None


def get_nlp(sentiment_model: str, zero_shot_model: str) -> "NLP":
    """Lazy-loaded singleton. Models load on first analyze request, not at server startup."""
    global _nlp_instance
    if _nlp_instance is None:
        _nlp_instance = NLP(sentiment_model, zero_shot_model)
    return _nlp_instance


class NLP:
    def __init__(self, sentiment_model: str, zero_shot_model: str):
        self._use_transformers = pipeline is not None
        self.sentiment = None
        self.zs = None
        if self._use_transformers:
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
        if self._use_transformers and self.sentiment and self.zs:
            return self._analyze_with_transformers(text, topk)
        return self._analyze_with_keyword_fallback(text, topk)

    def _analyze_with_transformers(self, text: str, topk: int) -> Tuple[str, str, List[str], List[str]]:
        clipped = text[:512]
        s = self.sentiment(clipped)[0]["label"].lower()
        e = self.zs(clipped, self.emotions)
        f = self.zs(clipped, self.facets)
        d = self.zs(clipped, self.distortions)
        emo = e["labels"][:topk]
        facets = f["labels"][:topk]
        dists = d["labels"][:topk]
        emotion = emo[0] if emo else "neutral"
        return s, emotion, facets, dists

    def _analyze_with_keyword_fallback(self, text: str, topk: int) -> Tuple[str, str, List[str], List[str]]:
        lowered = text.lower()
        positive_hits = self._count_hits(
            lowered,
            ["good", "great", "happy", "grateful", "relieved", "proud", "excited", "hopeful"],
        )
        negative_hits = self._count_hits(
            lowered,
            ["bad", "stressed", "sad", "angry", "anxious", "overwhelmed", "panic", "upset", "worried"],
        )
        sentiment = "positive" if positive_hits > negative_hits else "negative" if negative_hits > 0 else "neutral"

        emotion_map = {
            "anxiety": ["anxious", "panic", "worried", "nervous"],
            "overwhelm": ["overwhelmed", "too much", "burnout", "drained"],
            "sadness": ["sad", "down", "empty", "hopeless"],
            "anger": ["angry", "furious", "mad", "irritated"],
            "fear": ["afraid", "scared", "fear", "terrified"],
            "loneliness": ["lonely", "isolated", "alone"],
            "frustration": ["frustrated", "stuck", "blocked"],
            "joy": ["joy", "happy", "excited", "glad"],
        }
        emotion = self._top_label_from_map(lowered, emotion_map) or ("joy" if sentiment == "positive" else "anxiety")

        facet_map = {
            "work": ["work", "job", "boss", "office", "career"],
            "study": ["study", "exam", "school", "class", "assignment", "deadline"],
            "family": ["family", "parent", "sibling", "home"],
            "relationship": ["partner", "relationship", "boyfriend", "girlfriend", "spouse"],
            "health": ["health", "pain", "exercise", "diet", "sick"],
            "money": ["money", "rent", "bills", "debt", "financial"],
            "sleep": ["sleep", "insomnia", "tired", "rest"],
            "time-management": ["time", "schedule", "late", "procrastinating"],
            "motivation": ["motivation", "discipline", "drive"],
            "confidence": ["confidence", "self-esteem", "insecure"],
            "social": ["friend", "social", "people", "party"],
            "focus": ["focus", "distracted", "concentrate", "attention"],
        }

        distortion_map = {
            "catastrophizing": ["disaster", "ruined", "worst-case", "everything is over"],
            "overgeneralization": ["always", "never", "every time"],
            "personalization": ["my fault", "because of me", "i caused"],
            "mind-reading": ["they think", "everyone thinks", "they must think"],
            "all-or-nothing": ["all or nothing", "completely", "total failure"],
            "should-statements": ["should", "must", "supposed to"],
            "fortune-telling": ["will fail", "going to fail", "it will go badly"],
            "filtering": ["only bad", "nothing good", "all negative"],
        }

        facets = self._top_labels(lowered, facet_map, topk, self.facets)
        distortions = self._top_labels(lowered, distortion_map, topk, self.distortions)
        return sentiment, emotion, facets, distortions

    @staticmethod
    def _count_hits(text: str, keywords: Sequence[str]) -> int:
        return sum(1 for keyword in keywords if keyword in text)

    def _top_label_from_map(self, text: str, label_map: dict[str, Sequence[str]]) -> str:
        labels = self._top_labels(text, label_map, 1, self.emotions)
        return labels[0] if labels else ""

    def _top_labels(
        self,
        text: str,
        label_map: dict[str, Sequence[str]],
        topk: int,
        fallback_pool: Sequence[str],
    ) -> List[str]:
        scores = []
        for label, words in label_map.items():
            score = self._count_hits(text, words)
            if score > 0:
                scores.append((label, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        labels = [label for label, _ in scores[:topk]]
        if len(labels) < topk:
            for item in fallback_pool:
                if item not in labels:
                    labels.append(item)
                if len(labels) == topk:
                    break
        return labels

