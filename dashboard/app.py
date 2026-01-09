import sys
import os

# --------------------------------------------------
# Make project root importable
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- INTERNAL MODULES -----------------
from llms.csv_to_json import convert_csv_to_json
from utils.finance_engine import generate_financial_analysis
from utils.strategy_engine import generate_strategy_analysis
from utils.marketing_engine import generate_marketing_analysis
from utils.llm_narrative_engine import (
    generate_financial_narrative,
    generate_strategy_narrative,
    generate_marketing_narrative,
    generate_ceo_narrative
)
import importlib
import sys

# Force reload of report module to avoid caching issues
if 'reports.generate_report' in sys.modules:
    importlib.reload(sys.modules['reports.generate_report'])

from reports.generate_report import generate_report
from reports.generate_ppt import generate_ppt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Intelligent Business Strategy Orchestrator",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING (EXECUTIVE / POWER BI FEEL)
# --------------------------------------------------
st.markdown("""
<style>
.insight-card {
    background-color: #111827;
    padding: 18px;
    border-left: 6px solid #3b82f6;
    border-radius: 10px;
    margin-bottom: 18px;
}
.section-space {
    margin-top: 28px;
}
.small-note {
    color: #9ca3af;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR — DATA INPUT
# ==================================================
st.sidebar.title("📂 Data Input")

uploaded_business = st.sidebar.file_uploader(
    "Upload Business Data (CSV)",
    type=["csv"]
)

uploaded_pl = st.sidebar.file_uploader(
    "Upload Profit & Loss Data (CSV)",
    type=["csv"],
    key="pl"
)

# ---------------- LOAD BUSINESS DATA ----------------
if uploaded_business:
    with open("data/uploaded_business.csv", "wb") as f:
        f.write(uploaded_business.getbuffer())
    company = convert_csv_to_json("data/uploaded_business.csv")
else:
    company = json.load(open("data/company_data.json"))

# ---------------- LOAD P&L DATA ----------------
pl_df = pd.read_csv(uploaded_pl) if uploaded_pl else pd.read_csv("data/profit_loss.csv")

# ==================================================
# BASIC VARIABLES
# ==================================================
revenue = company.get("revenue", 0)
expenses = company.get("expenses", 0)
profit = revenue - expenses
growth = company.get("growth_rate", "N/A")
team_size = company.get("team_size", "N/A")

# ==================================================
# HEADER
# ==================================================
st.title("🧠 Intelligent Business Strategy Orchestrator")
st.caption(
    "AI-driven, MBA-style executive decision system • "
    "Data-first • Human-like reasoning • CEO-level synthesis"
)

# ==================================================
# KPI ROW (EXECUTIVE SNAPSHOT)
# ==================================================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"₹ {revenue:,}")
c2.metric("Expenses", f"₹ {expenses:,}")
c3.metric("Profit / Loss", f"₹ {profit:,}")
c4.metric("Team Size", team_size)

# ==================================================
# FINANCIAL ANALYSIS
# ==================================================
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
st.subheader("💰 Financial Health & Risk")

financial_metrics, _ = generate_financial_analysis(company, pl_df)
financial_text = generate_financial_narrative(company, financial_metrics)

st.markdown(
    f"<div class='insight-card'><b>Key Financial Insight</b><br>{financial_text.split('.')[0]}.</div>",
    unsafe_allow_html=True
)

col_text, col_chart = st.columns([2, 1])

with col_text:
    with st.expander("📘 Detailed Financial Explanation"):
        st.write(financial_text)

with col_chart:
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(pl_df["Month"], pl_df["Revenue"], label="Revenue")
    ax.plot(pl_df["Month"], pl_df["Expenses"], label="Expenses")
    ax.legend()
    st.pyplot(fig)

# ==================================================
# STRATEGY ANALYSIS
# ==================================================
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
st.subheader("📈 Strategy Direction")

strategy = generate_strategy_analysis(company, financial_metrics)
strategy_text = generate_strategy_narrative(company, strategy, financial_metrics)

st.markdown(
    f"<div class='insight-card'><b>Strategic Direction</b><br>{strategy_text.split('.')[0]}.</div>",
    unsafe_allow_html=True
)

col_text, col_chart = st.columns([2, 1])

with col_text:
    with st.expander("📘 Strategy Reasoning"):
        st.write(strategy_text)

with col_chart:
    strategy_df = pd.DataFrame({
        "Focus Area": strategy["focus_areas"],
        "Priority": list(range(len(strategy["focus_areas"]), 0, -1))
    })
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.barh(strategy_df["Focus Area"], strategy_df["Priority"])
    st.pyplot(fig)

# ==================================================
# MARKETING ANALYSIS
# ==================================================
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
st.subheader("📣 Marketing Performance")

marketing = generate_marketing_analysis(company, pl_df)
marketing_text = generate_marketing_narrative(marketing)

st.markdown(
    f"<div class='insight-card'><b>Marketing Insight</b><br>{marketing_text.split('.')[0]}.</div>",
    unsafe_allow_html=True
)

col_text, col_table = st.columns([2, 1])

with col_text:
    with st.expander("📘 Marketing Explanation"):
        st.write(marketing_text)

with col_table:
    roi_df = pd.DataFrame.from_dict(
        marketing["roi"], orient="index", columns=["ROI (%)"]
    ).sort_values("ROI (%)", ascending=False)

    st.markdown("**ROI Snapshot**")
    st.table(
        roi_df.style.highlight_max(axis=0, color="#2563eb")
    )

# ==================================================
# CEO SYNTHESIS
# ==================================================
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
st.subheader("🧠 Executive Direction & Strategic Priorities")


ceo_text = generate_ceo_narrative(company, financial_metrics, strategy, marketing)

st.markdown(
    f"<div class='insight-card'><b>CEO Summary</b><br>{ceo_text.split('.')[0]}.</div>",
    unsafe_allow_html=True
)

with st.expander("📘 Full CEO Decision Memo"):
    st.write(ceo_text)

# ==================================================
# REPORTS
# ==================================================
st.markdown("<div class='section-space'></div>", unsafe_allow_html=True)
st.subheader("📄 Executive Deliverables")

col_pdf, col_ppt = st.columns(2)

with col_pdf:
    if st.button("📘 Generate Detailed PDF Report"):
        pdf_path = generate_report(
            company,
            {
                "finance_output": financial_text,
                "strategy_output": strategy_text,
                "marketing_output": marketing_text,
                "final_decision": ceo_text,
                "hr_output": f"Current team size: {team_size}"
            },
            pl_df=pl_df,
            financial_metrics=financial_metrics
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name="Executive_Business_Report.pdf",
                mime="application/pdf"
            )

with col_ppt:
    if st.button("📊 Generate Executive PPT"):
        # Clean ceo_text before splitting
        import re
        clean_ceo = re.sub(r'\*+', '', ceo_text)  # Remove all asterisks
        clean_ceo = re.sub(r'\s+', ' ', clean_ceo)  # Clean spaces
        ceo_sentences = [s.strip() for s in clean_ceo.split(".") if s.strip()][:3]
        
        # Clean strategy focus areas
        clean_strategy = []
        for item in strategy["focus_areas"]:
            clean_item = re.sub(r'\*+', '', str(item))
            clean_item = re.sub(r'\s+', ' ', clean_item).strip()
            if clean_item:
                clean_strategy.append(clean_item)
        
        ppt_path = generate_ppt(
            company,
            {
                "risk": financial_metrics["risk_level"],
                "strategy_focus": clean_strategy,
                "ceo_summary": ceo_sentences
            }
        )
        with open(ppt_path, "rb") as f:
            st.download_button(
                "⬇️ Download PPT",
                f,
                file_name="Executive_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption(
    "🧠 Intelligent Business Strategy Orchestrator • "
    "Designed like a real MBA / consulting management cockpit"
)
