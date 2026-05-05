import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def dashboard():
    nav_items = [
        {"label": "Dashboard", "href": "/"},
        {"label": "API Health", "href": "/health-check"},
    ]
    return render_template("dashboard.html", nav_items=nav_items, active_path=request.path)


@app.get("/health-check")
def health_check():
    payload = {"frontend_status": "ok"}
    return jsonify(payload), 200


if __name__ == "__main__":
    raise SystemExit("Run this app with Gunicorn: gunicorn --bind 0.0.0.0:5010 app:app")
