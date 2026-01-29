
import streamlit as st
import pandas as pd
import time
from src.logic.processor import ClaimProcessor

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ayushma - Smart Pre-Audit",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME CONSTANTS ---
PRIMARY_COLOR = "#2563EB"
BG_COLOR = "#0F172A"
SEC_BG_COLOR = "#1E293B"
TEXT_COLOR = "#F8FAFC"
ACCENT_COLOR = "#22C55E"

# --- CUSTOM CSS ---
st.markdown(f"""
<style>
    /* Global Text & Background */
    [data-testid="stAppViewContainer"] {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
    }}
    [data-testid="stSidebar"] {{
        background-color: {SEC_BG_COLOR};
        border-right: 1px solid #334155;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, label {{
        font-family: 'Inter', sans-serif !important;
        color: {TEXT_COLOR} !important;
    }}
    .stMarkdown p {{
        color: #CBD5F1 !important;
    }}

    /* Widget Visibility Fixes (Dark Mode) */
    .stFileUploader label {{
        color: {TEXT_COLOR} !important;
        font-weight: 600;
    }}
    [data-testid="stFileUploader"] {{
        background-color: {SEC_BG_COLOR};
        padding: 1rem;
        border-radius: 8px;
        border: 1px dashed #475569;
    }}
    [data-testid="stFileUploader"] small {{
        color: #94A3B8 !important; /* Muted text for drag/drop instructions */
    }}
    
    .stSelectbox label, .stToggle label {{
        color: {TEXT_COLOR} !important;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {SEC_BG_COLOR} !important;
        color: {TEXT_COLOR} !important;
        border-radius: 8px;
    }}
    [data-testid="stExpanderDetails"] {{
        background-color: {BG_COLOR};
        border-color: {SEC_BG_COLOR};
    }}

    /* Header Component */
    .header-container {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        border: 1px solid #1e40af;
    }}
    .header-title {{
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
    }}
    .header-subtitle {{
        font-size: 1.1rem;
        color: #bfdbfe;
        margin-top: 0.5rem;
    }}

    /* Card Component */
    .css-card {{
        background-color: {SEC_BG_COLOR};
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
    }}
    .css-card h3 {{
        margin-top: 0;
        font-size: 1.25rem;
    }}

    /* Status Badges */
    .status-box {{
        padding: 1.25rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        border: 1px solid transparent;
    }}
    .status-clean {{
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80 !important;
        border-color: rgba(34, 197, 94, 0.3);
    }}
    .status-clean h2 {{ color: #4ade80 !important; }}
    
    .status-partial {{
        background-color: rgba(234, 179, 8, 0.15);
        color: #facc15 !important;
        border-color: rgba(234, 179, 8, 0.3);
    }}
    .status-partial h2 {{ color: #facc15 !important; }}

    .status-review {{
        background-color: rgba(239, 68, 68, 0.15);
        color: #f87171 !important;
        border-color: rgba(239, 68, 68, 0.3);
    }}
    .status-review h2 {{ color: #f87171 !important; }}

    /* Buttons */
    .stButton>button {{
        width: 100%;
        background-color: {PRIMARY_COLOR};
        color: white !important;
        height: 3rem;
        font-size: 1.1rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: #3b82f6;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: #F8FAFC !important;
        font-size: 1.8rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #94a3b8 !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4006/4006511.png", width=70)
    st.markdown("## Ayushma\n**AI Pre-Audit Assistant**")
    st.markdown("---")
    st.markdown("### 🛠 Tools")
    st.selectbox("Model Version", ["Ayushma-v1.0 (Rule Engine)", "Ayushma-v2.0 (LLM - Coming Soon)"])
    st.toggle("Advanced Debug Mode", value=False)
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.caption("Claims Processed Today: **12**")
    st.caption("Success Rate: **85%**")
    
    st.markdown("---")
    st.success("✅ System Operational")

# --- MAIN LAYOUT ---

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">Ayushma Audit</div>
    <div class="header-subtitle">Intelligent PM-JAY Claim Verification & Pre-Submission Analysis</div>
</div>
""", unsafe_allow_html=True)

processor = ClaimProcessor()

# Two-column Layout
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("📤 Document Upload")
    st.markdown("Please provide the required proofs for claim substantiation.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Grouping inputs
    with st.expander("📝 1. Clinical Documents (Required)", expanded=True):
        clinical_notes = st.file_uploader("Clinical Notes", type=["txt", "pdf", "png", "jpg", "jpeg"], key="notes")
        discharge_summary = st.file_uploader("Discharge Summary", type=["txt", "pdf", "png", "jpg", "jpeg"], key="disch")

    with st.expander("📸 2. Support Evidence (Required)", expanded=True):
        photos = st.file_uploader("Treatment Photographs", type=["png", "jpg", "jpeg", "pdf"], key="photos")
        hospital_bill = st.file_uploader("Hospital Bill", type=["txt", "pdf", "png", "jpg", "jpeg"], key="bill")
    
    # Calculate status
    files_status = {
        "Clinical Notes": clinical_notes is not None,
        "Discharge Summary": discharge_summary is not None,
        "Treatment Photographs": photos is not None,
        "Hospital Bill": hospital_bill is not None
    }
    missing_docs = [k for k, v in files_status.items() if not v]
    missing_count = len(missing_docs)
    
    # Run Button
    st.markdown("<br>", unsafe_allow_html=True)
    btn_text = f"🚀 Run Pre-Audit ({4-missing_count}/4 Ready)"
    run_btn = st.button(btn_text, type="primary", use_container_width=True)


with col_output:
    if run_btn:
        with st.spinner("🤖 Ayushma is analyzing claim data..."):
            time.sleep(1.5) # UX Loading
            
            # Prepare contents
            file_contents = {}
            
            def safe_read(uploaded_file):
                if uploaded_file.type == "text/plain":
                    return uploaded_file.getvalue().decode("utf-8")
                else:
                    return f"[Binary File: {uploaded_file.name}]" # Placeholder for non-txt files in POC
            
            if clinical_notes: file_contents["notes"] = safe_read(clinical_notes)
            if discharge_summary: file_contents["summary"] = safe_read(discharge_summary)
            if hospital_bill: file_contents["bill"] = safe_read(hospital_bill)
            
            # Process Logic
            extracted = processor.extract_information(file_contents)
            results = processor.validate_claim(files_status, extracted)
            
            # Styles
            status = results["overall_status"]
            style_class = "status-clean" if status == "CLEAN" else "status-partial" if status == "PARTIAL_APPROVAL" else "status-review"
            icon = "✅" if status == "CLEAN" else "⚠️" if status == "PARTIAL_APPROVAL" else "🛑"
            
            # 1. Overall Status
            st.markdown(f"""
            <div class="css-card">
                <div class="status-box {style_class}">
                    <h2 style="margin:0; font-size:1.8rem;">{icon} {status.replace('_', ' ')}</h2>
                    <p style="margin:0.5rem 0 0 0; opacity:0.9;">{results['reason']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Financial Metrics
            st.markdown("### 💰 Financial Analysis")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Claims", f"₹{results['billed_amount']:,}", help="Total amount claimed by hospital")
            with m2:
                st.metric("Approved", f"₹{results['approved_amount']:,}", help="Amount eligible under PM-JAY package")
            with m3:
                delta = results['billed_amount'] - results['approved_amount']
                val_color = "normal" if delta == 0 else "inverse"
                st.metric("Disallowed", f"₹{results['flagged_amount']:,}", delta=-delta if delta > 0 else 0, delta_color=val_color)
            
            st.markdown("---")

            # 3. Recommendations
            if results["recommendations"]:
                st.markdown("### 📋 Action Plan")
                for rec in results["recommendations"]:
                    st.warning(f"**Action Required**: {rec}")
            
            # 4. Deep Dive
            with st.expander("🔍 Deep Dive Analysis"):
                st.markdown(f"**Selected Package**: `{results['selected_package_code']}`")
                st.markdown("**Evidence Checklist**:")
                for doc, present in files_status.items():
                    st.markdown(f"- {'✅' if present else '❌'} {doc}")
                st.markdown("---")
                st.caption("Extracted Data JSON:")
                st.json(extracted)

    else:
        # Empty State
        st.markdown(f"""
        <div class="css-card" style="text-align: center; color: #94a3b8; padding: 4rem;">
            <h3>👋 Ready to Audit</h3>
            <p style="color: #94a3b8;">Upload documents on the left and click <b>Run Pre-Audit</b> to see results here.</p>
        </div>
        """, unsafe_allow_html=True)
