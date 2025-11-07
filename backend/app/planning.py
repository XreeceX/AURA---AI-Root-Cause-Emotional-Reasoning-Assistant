def plan_7day(emotion, facets, distortions, causes):
    goals = []
    actions = []
    coping = []
    reflect = []
    metric = "daily-self-report-1-5"
    if "time-management" in facets:
        goals.append("reduce-overwhelm-by-structuring-day")
        actions += [
            {"day": 1, "task": "brain-dump-all-tasks-15m"},
            {"day": 1, "task": "sort-by-urgency-importance-10m"},
            {"day": 2, "task": "timebox-2-critical-tasks-2x45m"},
            {"day": 3, "task": "install-website-blocker-30m"},
            {"day": 4, "task": "schedule-buffer-2x15m"},
            {"day": 5, "task": "review-and-trim-20m"},
            {"day": 6, "task": "batch-similar-tasks-2x30m"},
            {"day": 7, "task": "weekly-retro-20m"}
        ]
    if "study" in facets:
        goals.append("improve-study-consistency-and-feedback")
        actions += [
            {"day": 1, "task": "define-2-specific-topics"},
            {"day": 2, "task": "active-recall-3x20m"},
            {"day": 3, "task": "spaced-repetition-30m"},
            {"day": 4, "task": "practice-questions-45m"},
            {"day": 5, "task": "seek-1-peer-or-ta-feedback"},
            {"day": 6, "task": "teach-back-10m"},
            {"day": 7, "task": "adjust-plan-15m"}
        ]
    if emotion in ["anxiety", "overwhelm", "fear"]:
        coping += ["paced-breathing-5-5-5", "worry-time-15m", "grounding-5-senses"]
    if "personalization" in distortions or "catastrophizing" in distortions:
        coping += ["thought-record-disputation-10m", "evidence-for-against-10m"]
    reflect = ["what-worked-today", "one-stressor-one-response"]
    return {
        "goals": list(dict.fromkeys(goals)),
        "actions": actions[:10],
        "coping": list(dict.fromkeys(coping)),
        "reflect": reflect,
        "metric": metric,
    }

