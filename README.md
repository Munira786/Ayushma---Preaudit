🏥 Ayushma – AI-Based Medical Insurance Claim Pre-Audit System

Ayushma is an AI-assisted medical insurance claim pre-audit system designed to reduce claim rejections and processing delays under PM-JAY (Ayushman Bharat).
It validates hospital claims before submission by checking medical severity, package code correctness, billing limits, and document completeness.

This project was built as a hackathon MVP focusing on correctness, explainability, and real-world feasibility.

🚩 Problem Statement

In India, 1 out of every 5 health insurance claims is rejected or delayed due to:

Incorrect package code selection

Billing amount exceeding policy limits

Missing or inconsistent documents

These issues cause:

Revenue loss for hospitals

Delayed patient discharge

High rework burden on billing staff

Ayushma solves this by acting as a pre-submission audit assistant.

💡 Solution Overview

Ayushma performs an automated pre-audit using AI-assisted rule validation.

Input Documents:

Clinical Notes – diagnosis & severity (e.g., % TBSA for burns)

Discharge Summary – treatment confirmation

Hospital Bill – package code & total amount

Photograph Evidence – treatment proof (demo purpose)

Output:

Suggested / validated PM-JAY package code

Approved amount based on policy limits

Flagged amount (if any)

Overall claim status:

CLEAN

PARTIAL_APPROVAL

REVIEW_REQUIRED

Clear explanations and recommendations

🧠 AI Logic (MVP)

Severity Extraction: Reads clinical notes to detect medical severity

Package Mapping: Maps severity to PM-JAY package slabs

Policy Validation:

Package code match

Billing limit check

Required document check

Explainable Output (no black-box decisions)

⚠️ This MVP uses a controlled AI + rule engine approach for reliability in hackathon demos.

🛠️ Tech Stack

Frontend: Streamlit (Python)

Backend Logic: Python

Policy Dataset: PM-JAY package slabs (sampled)

UI Design: Custom CSS (Light Theme)

Deployment: Local / Streamlit Cloud (optional)

📂 Test Documents (Demo Ready)

To ensure stable and predictable demo results, this repository includes a test_documents/ folder.

Folder Structure:
test_documents/
├── clean_claim/
│   ├── clinical_notes.txt
│   ├── discharge_summary.txt
│   ├── hospital_bill.txt
│   └── photo.jpg
├── partial_claim/
│   ├── clinical_notes.txt
│   ├── discharge_summary.txt
│   ├── hospital_bill.txt
│   └── photo.jpg
├── review_claim/
│   ├── clinical_notes.txt
│   ├── discharge_summary.txt
│   ├── hospital_bill.txt
│   └── photo.jpg

How to Use:

Upload files from:

clean_claim/ → CLEAN result

partial_claim/ → PARTIAL_APPROVAL

review_claim/ → REVIEW_REQUIRED

This helps judges test the system without ambiguity.

🚀 How to Run the Project
pip install streamlit
streamlit run app.py


Upload the required documents and click Run Pre-Audit.

🔮 Future Scope

Train ML models for severity extraction

OCR integration for scanned PDFs

Full PM-JAY policy ingestion using RAG

Secure backend APIs for hospital systems

DPDP Act compliant data handling

⚠️ Disclaimer

This project is an academic / hackathon proof-of-concept.
No real patient data is used.
Not intended for clinical or production use.

👩‍💻 Team

Project Lead: Munira Bhabarawala, Alefiya Bootwala
Domain: AI | Healthcare | Insurance Automation
