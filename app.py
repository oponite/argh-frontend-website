import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "25"))


def backend_endpoint(path):
    return f"{BACKEND_URL}/{path.lstrip('/')}"


@app.route("/")
def dashboard():
    nav_items = [
        {"label": "Dashboard", "href": "/"},
        {"label": "API Health", "href": "/health-check"},
    ]
    return render_template("dashboard.html", nav_items=nav_items, active_path=request.path)

@app.get("/health-check")
def health_check():
    payload = {"frontend_status": "ok", "backend_url": BACKEND_URL}
    try:
        response = requests.get(backend_endpoint("/health"), timeout=5)
        payload["backend_status"] = "ok" if response.ok else "error"
        payload["backend_response"] = response.json()
        return jsonify(payload), 200 if response.ok else 502
    except requests.RequestException as exc:
        payload["backend_status"] = "unreachable"
        payload["backend_error"] = str(exc)
        return jsonify(payload), 502
    except ValueError:
        payload["backend_status"] = "invalid_json"
        return jsonify(payload), 502


@app.post("/projection")
def projection():
    payload = request.get_json(silent=True) or {}
    away_team = payload.get("away_team")
    home_team = payload.get("home_team")
    try:
        if not away_team or not home_team:
            raise ValueError("Missing team values")
        response = requests.post(
            backend_endpoint("/api/basketball/projection"),
            json={
                "away_team": away_team,
                "home_team": home_team,
            },
            timeout=BACKEND_TIMEOUT,
        )
    except ValueError:
        return jsonify({"error": "Please provide both away and home teams."}), 400
    except requests.RequestException as exc:
        return jsonify({"error": f"Backend unavailable: {exc}"}), 502

    if not response.ok:
        try:
            error = response.json().get("detail", response.text)
        except ValueError:
            error = response.text
        return jsonify({"error": error}), response.status_code

    try:
        return jsonify(response.json())
    except ValueError:
        return jsonify({"error": "Backend returned invalid JSON."}), 502


if __name__ == "__main__":
    raise SystemExit("Run this app with Gunicorn: gunicorn --bind 0.0.0.0:5010 app:app")
