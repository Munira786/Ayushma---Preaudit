"""
Train text classification model: BM001A, BM001B, BM001C, BM001D.
TF-IDF + Logistic Regression. Saves model.pkl and vectorizer.pkl.
"""
import re
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Paths: backend/ml/ and backend/data/
ML_DIR = Path(__file__).resolve().parent
DATA_DIR = ML_DIR.parent / "data"
TRAINING_CSV = DATA_DIR / "training_data.csv"
MODEL_PATH = ML_DIR / "model.pkl"
VECTORIZER_PATH = ML_DIR / "vectorizer.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 1000


def _clean_text(text: str) -> str:
    """Clean for ML: lowercase, keep alphanumeric and %, normalize space."""
    if not isinstance(text, str) or not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9%\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def train():
    """Load CSV, train, save model.pkl and vectorizer.pkl. Deterministic."""
    print(f"[train] Loading data from {TRAINING_CSV}")
    if not TRAINING_CSV.exists():
        raise FileNotFoundError(f"Training data not found: {TRAINING_CSV}")

    df = pd.read_csv(TRAINING_CSV)
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV must have columns 'text' and 'label'")

    df = df.dropna(subset=["text", "label"])
    df["clean_text"] = df["text"].apply(_clean_text)
    print(f"[train] Samples: {len(df)}, labels: {df['label'].unique().tolist()}")

    X = df["clean_text"]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    vectorizer = TfidfVectorizer(max_features=MAX_FEATURES)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(random_state=RANDOM_STATE)
    clf.fit(X_train_vec, y_train)

    preds = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, preds)
    print(f"[train] Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    ML_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"[train] Saved {MODEL_PATH} and {VECTORIZER_PATH}")
    return acc


if __name__ == "__main__":
    train()
