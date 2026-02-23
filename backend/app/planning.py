from collections import defaultdict
from typing import Any, Dict, List


def plan_7day(emotion, facets, distortions, causes):
    goals = []
    actions = []
    coping = []
    reflect = ["what-worked-today", "one-stressor-one-response"]
    metric = "daily-self-report-1-5"
    facets_set = set(facets) if facets else set()

    if "time-management" in facets_set:
        goals.append("reduce-overwhelm-by-structuring-day")
        actions.extend([
            {"day": 1, "task": "brain-dump-all-tasks-15m"},
            {"day": 1, "task": "sort-by-urgency-importance-10m"},
            {"day": 2, "task": "timebox-2-critical-tasks-2x45m"},
            {"day": 3, "task": "install-website-blocker-30m"},
            {"day": 4, "task": "schedule-buffer-2x15m"},
            {"day": 5, "task": "review-and-trim-20m"},
            {"day": 6, "task": "batch-similar-tasks-2x30m"},
            {"day": 7, "task": "weekly-retro-20m"},
        ])
    if "study" in facets_set:
        goals.append("improve-study-consistency-and-feedback")
        actions.extend([
            {"day": 1, "task": "define-2-specific-topics"},
            {"day": 2, "task": "active-recall-3x20m"},
            {"day": 3, "task": "spaced-repetition-30m"},
            {"day": 4, "task": "practice-questions-45m"},
            {"day": 5, "task": "seek-1-peer-or-ta-feedback"},
            {"day": 6, "task": "teach-back-10m"},
            {"day": 7, "task": "adjust-plan-15m"},
        ])
    if "relationship" in facets_set or "social" in facets_set:
        goals.append("improve-communication-and-boundaries")
        actions.extend([
            {"day": 1, "task": "journal-one-conflict-10m"},
            {"day": 2, "task": "identify-your-boundary-needs"},
            {"day": 3, "task": "practice-one-boundary-assertion"},
            {"day": 4, "task": "schedule-quality-time-with-someone"},
            {"day": 5, "task": "reflect-on-communication-style"},
            {"day": 6, "task": "send-one-appreciation-message"},
            {"day": 7, "task": "review-and-adjust-approach"},
        ])
    if "health" in facets_set or "sleep" in facets_set:
        goals.append("improve-physical-and-sleep-habits")
        actions.extend([
            {"day": 1, "task": "log-sleep-and-energy-levels"},
            {"day": 2, "task": "set-consistent-wake-time"},
            {"day": 3, "task": "wind-down-routine-20m"},
            {"day": 4, "task": "10min-movement-or-stretch"},
            {"day": 5, "task": "review-sleep-log"},
            {"day": 6, "task": "no-screens-1hr-before-bed"},
            {"day": 7, "task": "plan-next-week-sleep-goals"},
        ])

    if not goals:
        goals.append("build-self-awareness-and-routine")
        default_tasks = [
            "reflection-and-gratitude-10m",
            "journal-one-emotion-5m",
            "mindful-break-5m",
            "review-priorities-10m",
            "one-small-win-today",
            "connect-with-nature-5m",
            "weekly-retro-15m",
        ]
        actions.extend([{"day": d, "task": t} for d, t in zip(range(1, 8), default_tasks)])

    if emotion in ["anxiety", "overwhelm", "fear"]:
        coping.extend(["paced-breathing-5-5-5", "worry-time-15m", "grounding-5-senses"])
    if "personalization" in distortions or "catastrophizing" in distortions:
        coping.extend(["thought-record-disputation-10m", "evidence-for-against-10m"])
    if not coping:
        coping.extend(["breathing-break-3m", "brief-walk-5m"])

    actions = _interleave_actions(actions)[:14]
    return {
        "goals": list(dict.fromkeys(goals)),
        "actions": actions,
        "coping": list(dict.fromkeys(coping)),
        "reflect": reflect,
        "metric": metric,
    }


def _interleave_actions(actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Distribute actions across days when multiple facet plans overlap."""
    by_day = defaultdict(list)
    for a in actions:
        by_day[a["day"]].append(a["task"])
    result = []
    for day in sorted(by_day.keys()):
        for task in by_day[day]:
            result.append({"day": day, "task": task})
    return result

