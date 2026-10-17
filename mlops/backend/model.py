"""Spam model: word and character TF-IDF features + logistic regression."""
import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "spam.csv"
MODEL_PATH = BASE_DIR / "models" / "spam_model_v2.joblib"


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "features",
                FeatureUnion(
                    [
                        (
                            "word",
                            TfidfVectorizer(
                                lowercase=True,
                                ngram_range=(1, 2),
                                sublinear_tf=True,
                            ),
                        ),
                        (
                            "char",
                            TfidfVectorizer(
                                analyzer="char_wb",
                                ngram_range=(3, 5),
                                min_df=2,
                                sublinear_tf=True,
                            ),
                        ),
                    ]
                ),
            ),
            ("clf", LogisticRegression(C=2, class_weight="balanced", max_iter=2000)),
        ]
    )


def load_dataset(path: Path = DATA_PATH):
    texts, labels = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(1 if row["label"].strip().lower() == "spam" else 0)
    return texts, labels


class SpamDetector:
    def __init__(self, data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH):
        self.data_path = Path(data_path)
        self.model_path = Path(model_path)
        if self.model_path.exists():
            self.pipeline = joblib.load(self.model_path)
        else:
            self.pipeline = self.train()

    def train(self) -> Pipeline:
        texts, labels = load_dataset(self.data_path)
        pipeline = build_pipeline().fit(texts, labels)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.model_path)
        return pipeline

    def predict(self, text: str) -> dict:
        spam_prob = float(self.pipeline.predict_proba([text])[0][1])
        is_spam = spam_prob >= 0.5
        return {
            "label": "spam" if is_spam else "ham",
            "is_spam": is_spam,
            "spam_probability": round(spam_prob, 4),
            "confidence": round(spam_prob if is_spam else 1 - spam_prob, 4),
        }


if __name__ == "__main__":  # python -m backend.model  -> (re)train and save
    SpamDetector().train()
    print(f"Model saved to {MODEL_PATH}")
