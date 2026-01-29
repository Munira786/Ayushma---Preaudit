
import re
from src.data.packages import PACKAGES, get_recommended_package

class ClaimProcessor:
    def __init__(self):
        pass

    def extract_information(self, files_content):
        """
        Simulates OCR/NLP extraction from provided file content strings.
        In a real system, this would use Tesseract or mapped NLP models.
        """
        extracted = {
            "tbsa": None,
            "stated_package": None,
            "billed_amount": None,
            "diagnosis_keywords": []
        }

        # Combine all text for simpler regexing in this POC
        full_text = " ".join(files_content.values())
        
        # 1. Extract TBSA (e.g., "30% TBSA", "Burns 45%")
        # Look for number followed by % or TBSA
        tbsa_match = re.search(r'(\d+)\s?%\s?(?:TBSA|burns)', full_text, re.IGNORECASE)
        if tbsa_match:
            extracted["tbsa"] = int(tbsa_match.group(1))

        # 2. Extract Package Code (e.g., "BM001A")
        pkg_match = re.search(r'(BM001[A-D])', full_text)
        if pkg_match:
            extracted["stated_package"] = pkg_match.group(1)

        # 3. Extract Billed Amount (e.g., "Total: 45000", "Amount: Rs. 45000")
        # specific keywords to avoid grabbing random numbers
        amt_match = re.search(r'(?:Total|Amount|Bill|Charges)\s?[:\-]?\s?(?:Rs\.?)?\s?(\d{3,6})', full_text, re.IGNORECASE)
        if amt_match:
            extracted["billed_amount"] = int(amt_match.group(1))

        return extracted

    def validate_claim(self, files_present, extracted_data):
        """
        Core logic to determine claim status.
        files_present: dict of {filename: boolean} or list of present types
        extracted_data: dict from extract_information
        """
        status = "processing"
        final_decision = "REVIEW_REQUIRED" # Default safe state
        reason = []
        recommendations = []
        
        # 1. Document Completeness Check
        required_docs = ["Clinical Notes", "Discharge Summary", "Treatment Photographs", "Hospital Bill"]
        missing_docs = [doc for doc in required_docs if not files_present.get(doc, False)]
        
        if missing_docs:
            reason.append(f"Missing mandatory documents: {', '.join(missing_docs)}.")
            recommendations.append("Upload all missing documents to proceed.")
            # If docs are missing, we immediately flag, but might still analyze available text
        
        tbsa = extracted_data.get("tbsa")
        stated_pkg_code = extracted_data.get("stated_package")
        billed_amt = extracted_data.get("billed_amount")

        approved_amt = 0
        flagged_amt = 0

        # 2. Clinical Validation (Package Selection)
        calculated_pkg = None
        if tbsa is not None:
            calculated_pkg = get_recommended_package(tbsa)
            if calculated_pkg:
                if stated_pkg_code:
                    if stated_pkg_code == calculated_pkg["code"]:
                        reason.append(f"Package code {stated_pkg_code} matches clinical severity ({tbsa}% TBSA).")
                    else:
                        reason.append(f"MISMATCH: Bill uses {stated_pkg_code}, but clinical notes indicate {calculated_pkg['code']} ({tbsa}% TBSA).")
                        recommendations.append(f"Correct package code to {calculated_pkg['code']} to match severity.")
                else:
                    reason.append(f"No package code found in bill. Recommended: {calculated_pkg['code']} ({tbsa}% TBSA).")
                    recommendations.append(f"Add package code {calculated_pkg['code']} to the final bill.")
            else:
                reason.append(f"Could not map TBSA {tbsa}% to a known package.")
        else:
            reason.append("Could not extract TBSA % from clinical notes. Cannot validate severity.")
            recommendations.append("Ensure Clinical Notes explicitly state burn percentage (e.g., '30% TBSA').")

        # 3. Financial Validation
        active_pkg = PACKAGES.get(stated_pkg_code) if stated_pkg_code else calculated_pkg
        
        if active_pkg and billed_amt:
            limit = active_pkg["max_amount"]
            if billed_amt <= limit:
                approved_amt = billed_amt
                reason.append(f"Billed amount (₹{billed_amt}) is within policy limit (₹{limit}).")
            else:
                approved_amt = limit
                flagged_amt = billed_amt - limit
                reason.append(f"OVERBILLING: Exceeds package limit of ₹{limit} by ₹{flagged_amt}.")
                recommendations.append(f"Reduce bill amount to ₹{limit} or provide justification for excess.")
                if final_decision != "REVIEW_REQUIRED": # Don't downgrade if already review needed
                    final_decision = "PARTIAL_APPROVAL"

        elif not billed_amt:
             reason.append("Could not extract total billed amount.")
             recommendations.append("Ensure Hospital Bill clearly identifies the Total Amount.")

        # Final Status Determination
        if missing_docs:
            final_decision = "REVIEW_REQUIRED"
        elif "MISMATCH" in str(reason) or "Could not extract" in str(reason):
            final_decision = "REVIEW_REQUIRED"
        elif flagged_amt > 0:
            final_decision = "PARTIAL_APPROVAL"
        else:
            final_decision = "CLEAN"

        return {
            "overall_status": final_decision,
            "selected_package_code": stated_pkg_code or (calculated_pkg["code"] if calculated_pkg else "N/A"),
            "billed_amount": billed_amt if billed_amt else 0,
            "approved_amount": approved_amt,
            "flagged_amount": flagged_amt,
            "missing_documents": missing_docs,
            "reason": " ".join(reason),
            "recommendations": recommendations
        }
