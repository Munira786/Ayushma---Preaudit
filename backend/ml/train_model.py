"""
ML training for package (BM001A–D) classification from clinical text.
TF-IDF + Logistic Regression; saves model, vectorizer, and metadata.
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# Import clean_text: from backend when run as package, else from parent path
_parent = Path(__file__).resolve().parent.parent
if _parent not in sys.path:
    sys.path.insert(0, str(_parent))
try:
    from backend.services.text_cleaner import clean_text
except ImportError:
    from services.text_cleaner import clean_text


def train(
    data_path: str | Path | None = None,
    model_dir: str | Path | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
    max_features: int = 1000,
) -> dict:
    """
    Load CSV (text, label), clean, vectorize, train, evaluate, save artifacts.
    Returns metrics dict: accuracy, report, n_samples, model_path, error (if any).
    """
    try:
        from backend import config as _cfg
        _config = _cfg
    except ImportError:
        _config = None
    base_dir = Path(__file__).resolve().parent
    data_path = Path(data_path) if data_path else (getattr(_config, "TRAINING_CSV", None) if _config else None) or (base_dir.parent / "data" / "training_data.csv")
    data_path = data_path.resolve()
    model_dir = Path(model_dir) if model_dir else (getattr(_config, "ML_DIR", None) if _config else None) or base_dir
    model_path = model_dir / "model.pkl"
    vec_path = model_dir / "vectorizer.pkl"
    metadata_path = model_dir / "metadata.json"

    if not data_path.exists():
        return {"ok": False, "error": f"Training data not found: {data_path}"}

    df = pd.read_csv(data_path)
    if "text" not in df.columns or "label" not in df.columns:
        return {"ok": False, "error": "CSV must have columns 'text' and 'label'"}

    df = df.dropna(subset=["text", "label"])
    n_samples = len(df)
    df["clean_text"] = df["text"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=test_size, random_state=random_state
    )

    vectorizer = TfidfVectorizer(max_features=max_features)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(random_state=random_state)
    clf.fit(X_train_vec, y_train)

    predictions = clf.predict(X_test_vec)
    accuracy = float(accuracy_score(y_test, predictions))
    report = classification_report(y_test, predictions, output_dict=True)

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vec_path)

    metadata = {
        "accuracy": accuracy,
        "n_samples": n_samples,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "model_path": str(model_path),
        "report": report,
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return {
        "ok": True,
        "accuracy": accuracy,
        "n_samples": n_samples,
        "report": report,
        "model_path": str(model_path),
        "metadata_path": str(metadata_path),
    }


if __name__ == "__main__":
    result = train()
    if result.get("ok"):
        print(f"Accuracy: {result['accuracy']:.4f}")
        print(f"Saved to {result['model_path']}")
    else:
        print("Error:", result.get("error"))
        sys.exit(1)
