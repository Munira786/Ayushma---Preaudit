
import unittest
from src.logic.processor import ClaimProcessor

class TestAyushmaLogic(unittest.TestCase):
    def setUp(self):
        self.processor = ClaimProcessor()
        self.files_all_present = {
            "Clinical Notes": True, "Discharge Summary": True,
            "Treatment Photographs": True, "Hospital Bill": True
        }

    def test_clean_claim(self):
        files = {
            "notes": "Diagnosis: Burns 30% TBSA.",
            "bill": "Package: BM001B. Total: 12000",
            "summary": "Discharged."
        }
        extracted = self.processor.extract_information(files)
        result = self.processor.validate_claim(self.files_all_present, extracted)
        self.assertEqual(result["overall_status"], "CLEAN")
        self.assertEqual(result["approved_amount"], 12000)

    def test_mismatch_claim(self):
        files = {
            "notes": "Diagnosis: Burns 5% TBSA.", # Should be BM001A
            "bill": "Package: BM001B. Total: 15000",
            "summary": "Discharged."
        }
        extracted = self.processor.extract_information(files)
        result = self.processor.validate_claim(self.files_all_present, extracted)
        self.assertEqual(result["overall_status"], "REVIEW_REQUIRED")
        self.assertTrue("MISMATCH" in result["reason"])

    def test_overbilling_claim(self):
        files = {
            "notes": "Diagnosis: Burns 30% TBSA.", # BM001B (Max 15000)
            "bill": "Package: BM001B. Total: 20000",
            "summary": "Discharged."
        }
        extracted = self.processor.extract_information(files)
        result = self.processor.validate_claim(self.files_all_present, extracted)
        self.assertEqual(result["overall_status"], "PARTIAL_APPROVAL")
        self.assertEqual(result["approved_amount"], 15000)
        self.assertEqual(result["flagged_amount"], 5000)

    def test_missing_docs(self):
        files_missing = {
            "Clinical Notes": True, "Discharge Summary": False, # Missing
            "Treatment Photographs": True, "Hospital Bill": True
        }
        files = {"notes": "30% TBSA", "bill": "BM001B Total: 12000"}
        extracted = self.processor.extract_information(files)
        result = self.processor.validate_claim(files_missing, extracted)
        self.assertEqual(result["overall_status"], "REVIEW_REQUIRED")
        self.assertTrue("Missing mandatory" in result["reason"])

if __name__ == '__main__':
    unittest.main()
