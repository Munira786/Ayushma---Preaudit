import json
from pathlib import Path

class PolicyValidator:
    def __init__(self):
        self.policy_path = Path(__file__).parent.parent / "data" / "pmjay_subset.json"
        self.policies = self._load_policies()

    def _load_policies(self):
        try:
            if not self.policy_path.exists():
                print(f"Warning: Policy file not found at {self.policy_path}")
                return {}
            with open(self.policy_path, "r") as f:
                data = json.load(f)
                # Ensure we handle list of packages
                return {pkg["package_code"]: pkg for pkg in data}
        except Exception as e:
            print(f"Error loading policies: {e}")
            return {}

    def validate_claim(self, package_code: str, billed_amount: float) -> dict:
        result = {
            "status": "REVIEW_REQUIRED",
            "approved_amount": 0.0,
            "flagged_amount": 0.0,
            "reason": ""
        }

        if not package_code:
            result["reason"] = "No package predicted"
            return result

        policy = self.policies.get(package_code)
        if not policy:
            result["reason"] = f"Unknown package code: {package_code}"
            return result

        max_amount = policy.get("max_amount", 0)

        if billed_amount <= max_amount:
            result["status"] = "CLEAN"
            result["approved_amount"] = float(billed_amount)
            result["reason"] = "Claim is within policy limits"
        else:
            result["status"] = "PARTIAL_APPROVAL"
            result["approved_amount"] = float(max_amount)
            result["flagged_amount"] = billed_amount - max_amount
            result["reason"] = f"Claim exceeds max limit of {max_amount}"

        return result
