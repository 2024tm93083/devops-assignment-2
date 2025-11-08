# tests/test_fitness.py
import json
from src import fitness
from src.fitness import add_session, get_sessions, summary, add_user, clear_all

def setup_function():
    clear_all()

def test_add_and_get_session():
    s = add_session("Workout", "Push-ups", 20, None)
    assert s["id"] == 1
    assert s["exercise"] == "Push-ups"
    assert get_sessions()[0]["exercise"] == "Push-ups"

def test_summary_totals():
    add_session("Workout", "Push-ups", 20)
    add_session("Warm-up", "Jog", 10)
    summ = summary()
    assert summ["total_minutes"] == 30
    assert summ["totals_by_category"]["Workout"] == 20
    assert summ["totals_by_category"]["Warm-up"] == 10

def test_calories_with_user():
    add_user("alice", 70)  # 70 kg
    s = add_session("Workout", "Squats", 30, "alice")
    assert s["calories"] is not None
    # approximate calories check (rough)
    assert float(s["calories"]) > 0
