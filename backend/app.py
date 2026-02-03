"""
Ayushma: AI medical insurance pre-audit system.
POST /audit: clinical_notes + hospital_bill -> predicted_package, status, approved_amount, flagged_amount.
No silent failures; demo-safe and deterministic.
"""
import re
from fastapi import FastAPI, File, UploadFile

from .ml.infer import predict_package
from .services.file_reader import read_file
from .services.policy_rules import validate

app = FastAPI(title="Ayushma", description="AI medical insurance pre-audit MVP", version="0.1.0")


def _extract_amount(text: str) -> float:
    """Extract total amount from bill text using regex (numbers with optional , and .)."""
    if not text:
        return 0.0
    matches = re.findall(r"(\d+(?:,\d{3})*(?:\.\d{2})?)", text)
    if not matches:
        return 0.0
    try:
        amounts = [float(m.replace(",", "")) for m in matches]
        total = max(amounts)
        print(f"[app] Extracted amount: {total}")
        return total
    except ValueError:
        return 0.0


@app.get("/")
def root():
    return {"status": "ok", "service": "Ayushma", "audit": "POST /audit"}


@app.post("/audit")
async def audit(
    clinical_notes: UploadFile = File(...),
    discharge_summary: UploadFile = File(None),
    hospital_bill: UploadFile = File(...),
):
    """
    Pre-audit flow:
    1. Read clinical_notes text
    2. Predict package via ML
    3. Read hospital_bill text
    4. Extract total amount (regex)
    5. Validate via policy rules
    Returns: predicted_package, status, approved_amount, flagged_amount.
    """
    print("[app] /audit called")
    predicted_package = "BM001A"
    status = "PARTIAL_APPROVAL"
    approved_amount = 0.0
    flagged_amount = 0.0

    try:
        # 1. Read clinical notes (discharge_summary ignored for MVP)
        if discharge_summary:
            _ = await discharge_summary.read()
            print("[app] discharge_summary ignored for MVP")
        notes_bytes = await clinical_notes.read()
        notes_text = read_file(notes_bytes, clinical_notes.filename or "clinical_notes.txt")
        if not notes_text.strip():
            print("[app] WARNING: clinical_notes is empty; prediction may use default")

        # 2. Predict package via ML (do not block if severity missing)
        predicted_package = predict_package(notes_text)
        print(f"[app] predicted_package={predicted_package}")

        # 3. Read hospital bill
        bill_bytes = await hospital_bill.read()
        bill_text = read_file(bill_bytes, hospital_bill.filename or "hospital_bill.txt")

        # 4. Extract total amount
        billed_amount = _extract_amount(bill_text)

        # 5. Validate
        result = validate(predicted_package, billed_amount)
        status = result["status"]
        approved_amount = result["approved_amount"]
        flagged_amount = result["flagged_amount"]
        print(f"[app] status={status}, approved_amount={approved_amount}, flagged_amount={flagged_amount}")

    except Exception as e:
        print(f"[app] Audit failed: {e}")
        raise

    return {
        "predicted_package": predicted_package,
        "status": status,
        "approved_amount": approved_amount,
        "flagged_amount": flagged_amount,
    }
