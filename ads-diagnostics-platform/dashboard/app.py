import streamlit as st
import requests
import pandas as pd

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Ad Campaign Diagnostics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Ad Campaign Diagnostics Platform")

API_URL = "http://127.0.0.1:8000/diagnostics"

# ---- FETCH DATA FROM API ----
try:
    response = requests.get(API_URL)
    data = response.json()
except:
    st.error("⚠ Backend API is not running. Start FastAPI first.")
    st.stop()

issues = data["issues"]
total_issues = data["issues_detected"]

df = pd.DataFrame(issues)

# ---- ISSUE SEVERITY ----
severity_map = {
    "Low CTR": "Medium",
    "Budget exhausted": "High",
    "Possible conversion tracking failure": "Critical"
}

df["severity"] = df["issue"].map(severity_map)

# ---- METRICS ROW ----
col1, col2, col3 = st.columns(3)

col1.metric("Total Issues Detected", total_issues)
col2.metric("Unique Campaigns Affected", df["campaign_id"].nunique())
col3.metric("Issue Types", df["issue"].nunique())

st.divider()

# ---- SIDEBAR FILTER ----
st.sidebar.header("Filters")

issue_filter = st.sidebar.selectbox(
    "Select Issue Type",
    ["All"] + list(df["issue"].unique())
)

if issue_filter != "All":
    df = df[df["issue"] == issue_filter]

# ---- ISSUE DISTRIBUTION ----
st.subheader("Issue Distribution")

issue_counts = df["issue"].value_counts()

st.bar_chart(issue_counts)

st.divider()

# ---- SEVERITY BREAKDOWN ----
st.subheader("Issue Severity Breakdown")

severity_counts = df["severity"].value_counts()

st.bar_chart(severity_counts)

st.divider()

# ---- CAMPAIGN TABLE ----
st.subheader("Campaign Issues")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

st.divider()

# ---- CAMPAIGN INVESTIGATION ----
st.subheader("🔎 Investigate Campaign")

campaign_list = df["campaign_id"].unique()

selected_campaign = st.selectbox(
    "Select Campaign ID",
    campaign_list
)

campaign_data = df[df["campaign_id"] == selected_campaign]

st.dataframe(campaign_data, use_container_width=True)

st.divider()

st.divider()
st.subheader("🤖 AI Ads Troubleshooting Assistant (RAG)")

question = st.text_input("Ask about campaign issues")

if st.button("Ask AI"):
    
    response = requests.get(
        "http://127.0.0.1:8000/ask-rag",
        params={"question": question}
    )

    answer = response.json().get("answer", "No response generated.")

    st.success(answer)

st.divider()
st.subheader("📩 Support Ticket Simulator")

tickets = pd.read_csv("support_tickets.csv")

sample_ticket = st.selectbox(
    "Select Example Support Ticket",
    tickets["ticket_text"].unique()
)

if st.button("Diagnose Ticket"):

    response = requests.get(
        "http://127.0.0.1:8000/ask-rag",
        params={"question": sample_ticket}
    )

    answer = response.json().get("answer", "No response generated.")


    st.success(answer)

# ---- LOAD FULL DATASET ----
campaign_metrics = pd.read_csv("campaigns_dataset.csv")

st.subheader("Campaign Spend Distribution")

st.bar_chart(campaign_metrics["spend"].head(50))

