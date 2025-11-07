def hypothesize_causes(sentiment, emotion, facets, distortions):
    causes = []
    if sentiment == "negative":
        if "time-management" in facets:
            causes.append("overload-lack-structure")
        if "study" in facets:
            causes.append("skill-gap-or-unrealistic-goals")
        if "relationship" in facets:
            causes.append("miscommunication-or-boundary-issues")
        if emotion in ["anxiety", "fear", "overwhelm"]:
            causes.append("uncertainty-and-high-stakes")
        if "catastrophizing" in distortions:
            causes.append("threat-amplification")
        if "personalization" in distortions:
            causes.append("excessive-self-blame")
    if sentiment == "positive" and emotion in ["joy"]:
        causes.append("values-alignment")
    return list(dict.fromkeys(causes)) or ["insufficient-context"]

