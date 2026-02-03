"""
MVP Backend configuration: paths and ML settings.
"""
import os
from pathlib import Path

# Backend root
BACKEND_DIR = Path(__file__).resolve().parent
# Data
DATA_DIR = BACKEND_DIR / "data"
TRAINING_CSV = DATA_DIR / "training_data.csv"
# ML artifacts (model, vectorizer, metadata)
ML_DIR = BACKEND_DIR / "ml"
MODEL_PATH = ML_DIR / "model.pkl"
VECTORIZER_PATH = ML_DIR / "vectorizer.pkl"
METADATA_PATH = ML_DIR / "metadata.json"

# Training defaults
DEFAULT_TEST_SIZE = 0.2
DEFAULT_RANDOM_STATE = 42
DEFAULT_MAX_FEATURES = 1000
