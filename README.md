# Ayushma – AI-Based Medical Insurance Claim Pre-Audit System

Ayushma is an AI-assisted medical insurance claim **pre-audit system** designed to reduce claim rejections and delays under **PM-JAY (Ayushman Bharat)**.

The system checks hospital claims **before submission** by validating medical severity, insurance package codes, billing limits, and required documents.

This project is developed as a **hackathon MVP (proof of concept)**.

---

## Problem Statement

A significant number of health insurance claims in India are rejected or delayed due to:
- Incorrect PM-JAY package code selection  
- Billing amounts exceeding policy limits  
- Missing or inconsistent medical documents  

These issues lead to:
- Revenue loss for hospitals  
- Delayed patient discharge  
- Increased workload for billing staff  

---

## Proposed Solution

Ayushma acts as a **pre-audit assistant** for hospital billing teams.

Instead of submitting a claim directly to the insurer, the hospital uploads the claim documents to Ayushma, which identifies errors and mismatches **before submission**, reducing rejections and rework.

---

## Input Documents

Ayushma requires the following documents:
1. **Clinical Notes** – diagnosis and severity details  
2. **Discharge Summary** – treatment confirmation  
3. **Hospital Bill** – package code and total billed amount  
4. **Photograph Evidence** – treatment proof (demo purpose)

---

## System Functionality

Ayushma performs the following checks:
- Extracts medical severity from clinical notes (example: % TBSA for burns)
- Maps severity to the correct PM-JAY package code
- Validates:
  - Package code correctness
  - Billing amount within policy limits
  - Availability of all required documents
- Generates a structured **Pre-Audit Report**

---

## Output

The system generates:
- Suggested or validated PM-JAY package code  
- Approved claim amount  
- Flagged amount (if billing exceeds limit)  
- Overall claim status:
  - **CLEAN**
  - **PARTIAL_APPROVAL**
  - **REVIEW_REQUIRED**
- Clear reasons and recommendations for correction

---

## Technology Stack

- **Frontend:** Streamlit (Python)
- **Backend Logic:** Python
- **Policy Dataset:** PM-JAY package slabs (sampled)
- **UI:** Custom light-theme dashboard

---

## Test Documents (For Demo)

This repository includes a `test_documents/` folder to help evaluators test different claim scenarios.

### Folder Structure
test_documents/
├── clean_claim/
├── partial_claim/
├── review_claim/


Each folder contains:
- `clinical_notes.txt`
- `discharge_summary.txt`
- `hospital_bill.txt`
- `photo.jpg`

### Usage
- Upload files from **clean_claim/** → CLEAN result  
- Upload files from **partial_claim/** → PARTIAL_APPROVAL  
- Upload files from **review_claim/** → REVIEW_REQUIRED  

---

## How to Run the Project
pip install streamlit
streamlit run app.py

Upload all required documents and click Run Pre-Audit.

Future Scope<br>
1.Machine learning models for severity detection<br>
2.OCR support for scanned medical documents<br>
3.Full PM-JAY policy ingestion<br>
4.Secure backend APIs for hospital systems<br>
5.Compliance with India’s DPDP Act<br>

Disclaimer
1.This project is an academic / hackathon proof-of-concept.<br>
2.No real patient data is used.<br>
3.Not intended for clinical or production deployment.<br>

Author<br>
Munira Bhabarawala, Alefiya Bootwala<br>
Ayushma – AI-Based Medical Claim Pre-Audit System
