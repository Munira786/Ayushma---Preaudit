# 🏥 Ayushma – AI-Based Medical Insurance Claim Pre-Audit System

Ayushma is an AI-assisted medical insurance claim pre-audit system designed to reduce claim rejections and delays under PM-JAY (Ayushman Bharat).  
It validates hospital claims **before submission** by checking medical severity, package code correctness, billing limits, and document completeness.

This project is built as a **hackathon MVP** with a focus on reliability, explainability, and real-world feasibility.

---

## 🚩 Problem Statement

In India, nearly **1 out of every 5 healthcare insurance claims** is rejected or delayed due to:
- Incorrect package code selection  
- Billing amount exceeding policy limits  
- Missing or inconsistent documents  

These issues lead to:
- Revenue loss for hospitals  
- Delayed patient discharge  
- Heavy rework for billing staff  

Ayushma addresses this by performing a **pre-submission audit** of claims.

---

## 💡 Solution Overview

Ayushma works as an **AI-powered pre-audit assistant** for hospital billing teams.

### Input Documents
1. Clinical Notes (diagnosis and severity)
2. Discharge Summary
3. Hospital Bill (package code and total amount)
4. Photograph Evidence (for demo purpose)

### Output
- Validated or suggested PM-JAY package code  
- Approved claim amount based on policy limits  
- Flagged amount (if any)  
- Overall claim status:
  - CLEAN  
  - PARTIAL_APPROVAL  
  - REVIEW_REQUIRED  
- Clear reasons and recommendations for billing staff  

---

## 🧠 AI Logic (Hackathon MVP)

- Extracts medical severity from clinical notes (example: % TBSA for burns)
- Maps severity to PM-JAY package slabs
- Validates:
  - Package code correctness
  - Billing amount within policy limit
  - Presence of all required documents
- Produces **explainable results** instead of black-box decisions

This MVP uses a **controlled AI + rule-based engine** to ensure stable and predictable results during demos.

---

## 🛠️ Tech Stack

- Frontend: Streamlit (Python)
- Backend Logic: Python
- Policy Dataset: PM-JAY package slabs (sampled)
- UI: Custom CSS (Light Theme)
- Deployment: Local / Streamlit

---

## 📂 Test Documents (For Demo & Evaluation)

This repository includes a **test_documents/** folder to help evaluators easily test different claim scenarios.

### Folder Structure
