"""
Inference: predict package code from clinical text.
Exposes predict_package(text: str) -> str.
"""
import re
from pathlib import Path

import joblib

ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "model.pkl"
VECTORIZER_PATH = ML_DIR / "vectorizer.pkl"

# Default fallback if model missing or prediction fails
DEFAULT_PACKAGE = "BM001A"

_model = None
_vectorizer = None


def _clean_text(text: str) -> str:
    """Same as in train.py: lowercase, keep alphanumeric and %, normalize space."""
    if not isinstance(text, str) or not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9%\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _load_artifacts():
    global _model, _vectorizer
    if _model is not None and _vectorizer is not None:
        return
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        print(f"[infer] WARNING: Model not found at {MODEL_PATH}; using default {DEFAULT_PACKAGE}")
        return
    try:
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
        print(f"[infer] Loaded model and vectorizer from {ML_DIR}")
    except Exception as e:
        print(f"[infer] Failed to load model: {e}")


def predict_package(text: str) -> str:
    """
    Predict package code (BM001A, BM001B, BM001C, BM001D) from clinical text.
    Does not block if severity missing; returns default on failure.
    """
    _load_artifacts()
    if _model is None or _vectorizer is None:
        print("[infer] Using default package (model not loaded)")
        return DEFAULT_PACKAGE
    if not text or not str(text).strip():
        print("[infer] Empty text; using default package")
        return DEFAULT_PACKAGE
    try:
        clean = _clean_text(str(text))
        vec = _vectorizer.transform([clean])
        out = _model.predict(vec)[0]
        print(f"[infer] Predicted: {out}")
        return str(out)
    except Exception as e:
        print(f"[infer] Prediction error: {e}")
        return DEFAULT_PACKAGE
