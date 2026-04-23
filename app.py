import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


@app.route("/")
def dashboard():
    nav_items = [
        {"label": "Dashboard", "href": "/"},
        {"label": "API Health", "href": "/health-check"},
    ]
    return render_template("dashboard.html", nav_items=nav_items, active_path=request.path)

@app.get("/health-check")
def health_check():
    return jsonify({"frontend_status": "ok"})


@app.post("/projection")
def projection():
    payload = request.get_json(silent=True) or {}
    away_team = payload.get("away_team")
    home_team = payload.get("home_team")
    bookie_total = payload.get("bookie_total")

    try:
        if not away_team or not home_team:
            raise ValueError("Missing team values")
        response = requests.post(
            f"{BACKEND_URL}/api/basketball/projection",
            json={
                "away_team": away_team,
                "home_team": home_team,
                "bookie_total": float(bookie_total),
            },
            timeout=25,
        )
    except (TypeError, ValueError):
        return jsonify({"error": "Please provide away team, home team, and numeric bookie total."}), 400
    except requests.RequestException as exc:
        return jsonify({"error": f"Backend unavailable: {exc}"}), 502

    if not response.ok:
        return jsonify({"error": response.text}), response.status_code

    try:
        return jsonify(response.json())
    except ValueError:
        return jsonify({"error": "Backend returned invalid JSON."}), 502


if __name__ == "__main__":
    raise SystemExit("Run this app with Gunicorn: gunicorn --bind 0.0.0.0:5010 app:app")
