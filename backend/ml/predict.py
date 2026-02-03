import joblib
import joblib
import re
import os
import sys
from pathlib import Path

# Module-level cache
_model = None
_vectorizer = None

def reset_cache():
    """Clear loaded model/vectorizer so next prediction reloads from disk (e.g. after retrain)."""
    global _model, _vectorizer
    _model = None
    _vectorizer = None

def is_loaded():
    """Return True if model and vectorizer are loaded."""
    return _model is not None and _vectorizer is not None

def _load_artifacts():
    global _model, _vectorizer
    if _model is None:
        try:
            base_dir = Path(__file__).parent
            _model = joblib.load(base_dir / "model.pkl")
            _vectorizer = joblib.load(base_dir / "vectorizer.pkl")
        except Exception as e:
            print(f"Error loading ML artifacts: {e}")

# Allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.text_cleaner import clean_text

# Removed local clean_text function since we import it

def predict_package(text: str) -> str:
    _load_artifacts()
    if not _model or not _vectorizer:
        return "BM001A" # Fallback
    
    try:
        clean = clean_text(text)
        vec_text = _vectorizer.transform([clean])
        return _model.predict(vec_text)[0]
    except Exception as e:
        print(f"Prediction error: {e}")
        return "BM001A"
