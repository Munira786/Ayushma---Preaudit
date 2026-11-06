import streamlit as st
import pandas as pd
import time
import re
from sentence_transformers import SentenceTransformer, util

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ayushma - Smart Pre-Audit",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD DATASET ---
SPECIALITY_MAP = {
    "BM": "Burns & Plastic Surgery",
    "ER": "Emergency",
    "IN": "Interventional Neuroradiology",
    "MC": "Medical Cardiology",
    "MG": "General Medicine",
    "MM": "Mental Health",
    "MN": "Neonatology",
    "MO": "Medical Oncology",
}

@st.cache_data
def load_dataset():
    df = pd.read_csv("data/ayushman_packages.csv")
    # Derive speciality from the 2-letter prefix of package_id
    df["speciality"] = df["package_id"].str[:2].map(SPECIALITY_MAP).fillna("Other")
    return df

df = load_dataset()

# --- RULE ENGINE FUNCTIONS ---
def extract_tbsa(text):
    match = re.search(r'(\d+)\s*%', text)
    if match:
        return int(match.group(1))
    return None

def apply_burn_rules(input_text, predicted_package):
    tbsa = extract_tbsa(input_text)
    if tbsa is None:
        return predicted_package
        
    if tbsa <= 40:
        return "BM001B"
    elif 40 < tbsa <= 60:
        return "BM001C"
    elif tbsa > 60:
        return "BM001D"
        
    return predicted_package

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# Precompute embeddings
package_descriptions = df["package_description"].astype(str).tolist()
package_embeddings = model.encode(package_descriptions)

# --- THEME CONSTANTS ---
PRIMARY_COLOR = "#2563EB"
BG_COLOR = "#0F172A"
SEC_BG_COLOR = "#1E293B"
TEXT_COLOR = "#F8FAFC"
ACCENT_COLOR = "#22C55E"

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-color: {BG_COLOR};
    color: {TEXT_COLOR};
}}
[data-testid="stSidebar"] {{
    background-color: {SEC_BG_COLOR};
}}
h1,h2,h3,h4,p,label {{
    color:{TEXT_COLOR}!important;
}}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4006/4006511.png", width=70)
    st.markdown("## Ayushma\n**AI Pre-Audit Assistant**")
    st.markdown("---")
    st.selectbox("Model Version", ["Ayushma-v1.0 (AI Similarity Engine)"])
    st.toggle("Advanced Debug Mode", value=False)
    st.markdown("---")
    st.success("System Operational")

# --- HEADER ---
st.markdown("""
<div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);
padding:2rem;border-radius:12px;color:white;margin-bottom:2rem;">
<h2>Ayushma Audit</h2>
<p>Intelligent PM-JAY Claim Verification</p>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col_input, col_output = st.columns([1,1.2])

# ================= INPUT PANEL =================

with col_input:

    st.subheader("📤 Claim Information")

    clinical_notes = st.text_area(
        "Clinical Notes",
        height=150
    )

    discharge_summary = st.text_area(
        "Discharge Summary",
        height=150
    )

    treatment_photos = st.text_area(
        "Treatment Photograph Description",
        height=100
    )

    hospital_bill = st.text_area(
        "Hospital Bill Summary",
        height=120
    )

    generate = st.button("Generate Pre-Audit", use_container_width=True)

# ================= OUTPUT PANEL =================

with col_output:

    if generate:

        with st.spinner("Analyzing claim with AI..."):

            # Combine input text
            input_text = f"""
            Clinical Notes: {clinical_notes}
            Discharge Summary: {discharge_summary}
            Treatment Photos: {treatment_photos}
            Hospital Bill: {hospital_bill}
            """

            # Encode user input
            query_embedding = model.encode(input_text)

            # Calculate similarity
            scores = util.cos_sim(query_embedding, package_embeddings)
            best_index = scores.argmax().item()
            confidence = float(scores[0][best_index])
            best_package = df.iloc[best_index]
            predicted_package = best_package["package_id"]

            # --- APPLY RULE ENGINE ---
            predicted_package = apply_burn_rules(input_text, predicted_package)

            # Reload correct package details after rule correction
            package_row = df[df["package_id"] == predicted_package].iloc[0]

            approved_amount = package_row["package_amount"]
            speciality = package_row["speciality"]
            description = package_row["package_description"]

            # --- AUDIT DECISION ENGINE ---
            has_clinical_notes = bool(clinical_notes.strip())
            has_discharge_summary = bool(discharge_summary.strip())
            has_treatment_photos = bool(treatment_photos.strip())
            has_hospital_bill = bool(hospital_bill.strip())

            disapproval_reasons = []
            flag_reasons = []

            # Confidence thresholds
            if confidence < 0.30:
                disapproval_reasons.append(f"Claim description does not match any PM-JAY package (confidence: {confidence:.0%})")
            elif confidence < 0.45:
                flag_reasons.append(f"Low match confidence with PM-JAY packages ({confidence:.0%}) — manual review required")

            # Document checks
            if not has_clinical_notes and not has_discharge_summary:
                disapproval_reasons.append("Both Clinical Notes and Discharge Summary are missing — mandatory documents")
            else:
                if not has_clinical_notes:
                    flag_reasons.append("Clinical Notes are missing")
                if not has_discharge_summary:
                    flag_reasons.append("Discharge Summary is missing")
                if not has_treatment_photos:
                    flag_reasons.append("Treatment Photograph description is missing")
                if not has_hospital_bill:
                    flag_reasons.append("Hospital Bill Summary is missing")

            # Determine final verdict
            if disapproval_reasons:
                audit_verdict = "DISAPPROVED"
            elif flag_reasons:
                audit_verdict = "FLAGGED"
            else:
                audit_verdict = "APPROVED"

        # --- DISPLAY VERDICT ---
        if audit_verdict == "APPROVED":
            st.markdown("""
            <div style="background:linear-gradient(135deg,#14532d,#16a34a);
            padding:1.2rem 1.5rem;border-radius:10px;color:white;margin-bottom:1rem;">
            <h3 style="margin:0;color:white!important;">✅ CLAIM APPROVED</h3>
            <p style="margin:0.3rem 0 0;color:#bbf7d0!important;">Claim is valid under PM-JAY package</p>
            </div>""", unsafe_allow_html=True)
        elif audit_verdict == "FLAGGED":
            st.markdown("""
            <div style="background:linear-gradient(135deg,#713f12,#d97706);
            padding:1.2rem 1.5rem;border-radius:10px;color:white;margin-bottom:1rem;">
            <h3 style="margin:0;color:white!important;">⚠️ CLAIM FLAGGED — MANUAL REVIEW</h3>
            <p style="margin:0.3rem 0 0;color:#fde68a!important;">Claim requires manual review before approval</p>
            </div>""", unsafe_allow_html=True)
            for reason in flag_reasons:
                st.warning(f"⚠️ {reason}")
        else:  # DISAPPROVED
            st.markdown("""
            <div style="background:linear-gradient(135deg,#7f1d1d,#dc2626);
            padding:1.2rem 1.5rem;border-radius:10px;color:white;margin-bottom:1rem;">
            <h3 style="margin:0;color:white!important;">❌ CLAIM DISAPPROVED</h3>
            <p style="margin:0.3rem 0 0;color:#fecaca!important;">Claim does not meet PM-JAY eligibility criteria</p>
            </div>""", unsafe_allow_html=True)
            for reason in disapproval_reasons:
                st.error(f"❌ {reason}")

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Package Code", predicted_package)

        def format_amt(val):
            try:
                cleaned = str(val).replace(',', '').strip()
                return f"₹{float(cleaned):,.0f}"
            except (ValueError, TypeError):
                return "Variable (per day rate)"

        with col2:
            st.metric("Approved Amount", format_amt(approved_amount))

        with col3:
            st.metric("Match Confidence", f"{confidence:.0%}")

        st.markdown("---")

        st.markdown("### 🏥 Package Details")

        st.write(f"**Speciality:** {speciality}")
        st.write(f"**Description:** {description}")

        st.markdown("---")

        st.markdown("### 📄 Document Checklist")

        st.write("✅ Clinical Notes" if has_clinical_notes else "❌ Clinical Notes Missing")
        st.write("✅ Discharge Summary" if has_discharge_summary else "❌ Discharge Summary Missing")
        st.write("✅ Treatment Photos" if has_treatment_photos else "❌ Treatment Photos Missing")
        st.write("✅ Hospital Bill" if has_hospital_bill else "❌ Hospital Bill Missing")

    else:

        st.info("Upload claim information and click **Generate Pre-Audit**.")