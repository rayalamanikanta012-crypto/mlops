"""SIM - Flask frontend. Run: python -m frontend.app"""
import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)
app.config["API_URL"] = os.getenv("API_URL", "").rstrip("/")
app.config["API_PORT"] = os.getenv("API_PORT", "8000")


@app.route("/")
def index():
    return render_template(
        "index.html",
        api_url=app.config["API_URL"],
        api_port=app.config["API_PORT"],
        app_name="SIM",
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"},
    )
