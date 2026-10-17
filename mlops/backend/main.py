"""SIM - FastAPI backend. Run: uvicorn backend.main:app --reload"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.model import SpamDetector
from backend.schemas import EmailRequest, PredictionResponse

app = FastAPI(title="SIM Spam Detector API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = SpamDetector()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(email: EmailRequest):
    return detector.predict(f"{email.subject} {email.body}".strip())
