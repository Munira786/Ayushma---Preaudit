# Ayushma Backend (Hackathon MVP)

FastAPI backend for AI medical insurance pre-audit. Clean, reliable, demo-safe, deterministic.

## Structure

```
backend/
  app.py
  requirements.txt
  ml/
    train.py
    infer.py
  services/
    file_reader.py
    policy_rules.py
  data/
    training_data.csv
    pmjay_rules.json
```

## Setup

From **project root** (parent of `backend/`):

```bash
pip install -r backend/requirements.txt
```

## Train model (once)

From project root:

```bash
python -m backend.ml.train
```

Saves `backend/ml/model.pkl` and `backend/ml/vectorizer.pkl`.

## Run server

From project root:

```bash
python run_backend.py
```

Or: `uvicorn backend.app:app --host 127.0.0.1 --port 8000`

- API: http://127.0.0.1:8000  
- Docs: http://127.0.0.1:8000/docs  

## POST /audit

**Files (multipart):**

- `clinical_notes` (required) – TXT or PDF
- `discharge_summary` (optional, ignored for MVP)
- `hospital_bill` (required) – TXT or PDF

**Flow:** Read clinical notes → predict package (ML) → read bill → extract amount (regex) → validate (policy rules).

**Response:**

```json
{
  "predicted_package": "BM001A",
  "status": "CLEAN",
  "approved_amount": 12000.0,
  "flagged_amount": 0.0
}
```

- `status`: `CLEAN` or `PARTIAL_APPROVAL`
- Prediction is never blocked if severity is missing; default package used on failure.
- No silent failures; errors are raised and printed.
