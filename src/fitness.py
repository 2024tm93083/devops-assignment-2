# src/fitness.py
from datetime import datetime
from typing import List, Dict, Any, Optional

# Simple in-memory store (sufficient for assignment)
_SESSIONS: List[Dict[str, Any]] = []
_USER_INFO: Dict[str, Dict[str, Any]] = {}  # optional user data keyed by username

# MET default values by category (used if weight known)
MET_VALUES = {
    "Warm-up": 3.0,
    "Workout": 6.0,
    "Cool-down": 2.5
}

def add_user(username: str, weight_kg: float) -> None:
    """Optional: store basic user info (weight) for calories calc."""
    _USER_INFO[username] = {"weight_kg": float(weight_kg)}

def add_session(category: str, exercise: str, duration_minutes: int, username: Optional[str]=None) -> Dict[str, Any]:
    """Validate + add a session. Returns the stored session dict."""
    if not category or not exercise:
        raise ValueError("category and exercise are required")
    try:
        duration = int(duration_minutes)
    except Exception:
        raise ValueError("duration must be an integer (minutes)")

    if duration <= 0:
        raise ValueError("duration must be positive")

    timestamp = datetime.utcnow().isoformat()
    weight = None
    calories = None
    if username and username in _USER_INFO:
        weight = _USER_INFO[username].get("weight_kg")
    met = MET_VALUES.get(category, 5.0)
    if weight:
        # simple calories formula: (MET * 3.5 * weight_kg / 200) * duration
        calories = (met * 3.5 * weight / 200.0) * duration

    session = {
        "id": len(_SESSIONS) + 1,
        "category": category,
        "exercise": exercise,
        "duration": duration,
        "timestamp": timestamp,
        "username": username,
        "calories": round(calories, 1) if calories is not None else None
    }
    _SESSIONS.append(session)
    return session

def get_sessions() -> List[Dict[str, Any]]:
    """Return all sessions (copy)."""
    return list(_SESSIONS)

def summary() -> Dict[str, Any]:
    """Return aggregated totals."""
    totals = {}
    total_minutes = 0
    total_calories = 0.0
    calories_present = False
    for s in _SESSIONS:
        cat = s["category"]
        mins = s["duration"]
        totals.setdefault(cat, 0)
        totals[cat] += mins
        total_minutes += mins
        if s.get("calories") is not None:
            total_calories += float(s["calories"])
            calories_present = True

    result = {
        "totals_by_category": totals,
        "total_minutes": total_minutes
    }
    if calories_present:
        result["total_calories"] = round(total_calories, 1)
    return result

def clear_all() -> None:
    """Clear in-memory store (useful for tests)."""
    _SESSIONS.clear()
    _USER_INFO.clear()
