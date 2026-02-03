# 🏥 Ayushma – AI-Based Medical Insurance Claim Pre-Audit System

Ayushma is an AI-assisted medical insurance claim **pre-audit system** designed to reduce claim rejections and delays under **PM-JAY (Ayushman Bharat)** by validating claims **before submission**.

This project was built as a **hackathon MVP**, focusing on reliability, explainability, and real-world feasibility in healthcare systems.

---

## 🚨 Problem Statement

In India, a large percentage of health insurance claims are **rejected or delayed** due to:
- Incorrect package code selection  
- Missing or inconsistent documents  
- Billing amounts exceeding policy limits  

These issues increase hospital workload, delay patient discharge, and create financial stress.

---

## 💡 Solution Overview

Ayushma performs a **pre-submission audit** of medical insurance claims by:
- Analyzing clinical documents
- Validating PM-JAY package rules
- Flagging errors **before** final claim submission

The system helps hospitals correct mistakes early, reducing rejection rates.

---

## 🧠 How Ayushma Works

1. User uploads required documents:
   - Clinical Notes
   - Discharge Summary
   - Hospital Bill
   - Supporting Photographs

2. Ayushma:
   - Extracts relevant medical and billing information
   - Predicts an appropriate PM-JAY package (AI-assisted)
   - Validates billing amounts against policy limits

3. Generates a **Pre-Audit Report**:
   - CLEAN
   - PARTIAL APPROVAL
   - REVIEW REQUIRED

---

## ⚙️ Technology Stack

### Frontend
- **Streamlit (Python)**
- Custom CSS for modern UI

### Backend (MVP)
- Python-based audit engine
- Rule-based PM-JAY validation
- AI-assisted logic (demo-safe mode)

### AI / ML (Architecture)
- NLP-based package prediction (TF-IDF + Logistic Regression)
- Designed for future integration into live backend

---

## 📊 Key Features

- PM-JAY package validation
- Billing limit checks
- Missing document detection
- Explainable audit decisions
- Demo-safe and reliable execution

---

## 🧪 Demo Mode Note

For hackathon submission, the system runs in a **demo-safe audit mode** to ensure:
- Stable output
- No runtime failures
- Clear explanation of results

The backend architecture supports full ML inference and can be extended post-hackathon.

---

## 🔮 Future Enhancements

- Full ML-based severity prediction
- Image-based burn assessment
- Fraud and anomaly detection
- Integration with government health portals
- Real-time hospital system integration

---

## 👩‍💻 Team

**Project Name:** Ayushma  
**Domain:** Healthcare | Insurance | AI  
**Built for:** CSRBOX Hackathon  

---

## ⚠️ Disclaimer

This is an **academic proof-of-concept**.  
No real patient data is used.  
Not intended for clinical or legal decision-making.

---

## 📌 Repository

GitHub:  
https://github.com/Munira786/Ayushma---Preaudit
