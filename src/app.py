# src/app.py
from flask import Flask, request, jsonify
from src.fitness import add_session, get_sessions, summary, add_user, clear_all

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/users", methods=["POST"])
def create_user():
    payload = request.get_json() or {}
    username = payload.get("username")
    weight = payload.get("weight")
    if not username or weight is None:
        return jsonify({"error": "username and weight are required"}), 400
    try:
        add_user(username, float(weight))
        return jsonify({"msg": "user added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/sessions", methods=["POST"])
def create_session():
    payload = request.get_json() or {}
    category = payload.get("category")
    exercise = payload.get("exercise")
    duration = payload.get("duration")
    username = payload.get("username")
    if category is None or exercise is None or duration is None:
        return jsonify({"error": "category, exercise, duration are required"}), 400
    try:
        s = add_session(category, exercise, duration, username)
        return jsonify(s), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "internal error"}), 500

@app.route("/sessions", methods=["GET"])
def list_sessions():
    return jsonify(get_sessions()), 200

@app.route("/summary", methods=["GET"])
def get_summary():
    return jsonify(summary()), 200

# admin-only in-memory clear endpoint (for tests/demo) - not for prod
@app.route("/_clear", methods=["POST"])
def clear():
    clear_all()
    return jsonify({"msg": "cleared"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
