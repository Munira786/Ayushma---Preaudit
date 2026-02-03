"""
Policy validation: package_code + max_amount from pmjay_rules.json.
"""
import json
from pathlib import Path

# Path to rules file (backend/data/pmjay_rules.json)
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_RULES_PATH = _DATA_DIR / "pmjay_rules.json"

_rules_cache = None


def _load_rules():
    global _rules_cache
    if _rules_cache is not None:
        return _rules_cache
    if not _RULES_PATH.exists():
        print(f"[policy_rules] WARNING: Rules file not found at {_RULES_PATH}")
        _rules_cache = {}
        return _rules_cache
    try:
        with open(_RULES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        _rules_cache = {r["package_code"]: r for r in data if "package_code" in r and "max_amount" in r}
        print(f"[policy_rules] Loaded {len(_rules_cache)} rules from {_RULES_PATH}")
        return _rules_cache
    except Exception as e:
        print(f"[policy_rules] Failed to load rules: {e}")
        _rules_cache = {}
        return _rules_cache


def validate(package_code: str, billed_amount: float) -> dict:
    """
    Validate claim: package_code vs billed_amount.
    Returns: status (CLEAN | PARTIAL_APPROVAL), approved_amount, flagged_amount.
    """
    rules = _load_rules()
    approved_amount = 0.0
    flagged_amount = 0.0
    status = "PARTIAL_APPROVAL"

    if not package_code:
        print("[policy_rules] No package_code provided")
        return {"status": "PARTIAL_APPROVAL", "approved_amount": 0.0, "flagged_amount": billed_amount}

    r = rules.get(package_code)
    if not r:
        print(f"[policy_rules] Unknown package_code: {package_code}")
        return {"status": "PARTIAL_APPROVAL", "approved_amount": 0.0, "flagged_amount": billed_amount}

    max_amount = float(r.get("max_amount", 0))
    billed_amount = float(billed_amount)

    if billed_amount <= max_amount:
        status = "CLEAN"
        approved_amount = billed_amount
        flagged_amount = 0.0
        print(f"[policy_rules] CLEAN: {package_code} billed={billed_amount} <= max={max_amount}")
    else:
        approved_amount = max_amount
        flagged_amount = billed_amount - max_amount
        print(f"[policy_rules] PARTIAL_APPROVAL: {package_code} billed={billed_amount} > max={max_amount}, flagged={flagged_amount}")

    return {"status": status, "approved_amount": approved_amount, "flagged_amount": flagged_amount}
