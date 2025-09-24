import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# Load Data
# -----------------------------
st.set_page_config(page_title="Med-Sense AI Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("Sample_dataset_Proj.xlsx")
    return df

df = load_data()

# -----------------------------
# Risk Score Calculation
# -----------------------------
def compute_risk(row):
    score = 0
    if row['HR'] < 60 or row['HR'] > 100:
        score += 1
    if row['SpO₂'] < 95:
        score += 1
    if row['Temp'] < 36 or row['Temp'] > 37.5:
        score += 1
    if row['RR'] < 12 or row['RR'] > 20:
        score += 1

    # Add condition flags if present
    condition_cols = [c for c in df.columns if c not in ['Patient_ID','HR','SpO₂','Temp','RR']]
    for col in condition_cols:
        if row[col] == 1:
            score += 1
    return score

df['RiskScore'] = df.apply(compute_risk, axis=1)

def classify(score):
    if score <= 3:
        return "Stable"
    elif score <= 6:
        return "Moderate"
    else:
        return "Critical"

df['Status'] = df['RiskScore'].apply(classify)

# -----------------------------
# Dashboard Header
# -----------------------------
st.title("📊 Med-Sense AI – Remote Patient Monitoring Dashboard")

total_patients = len(df)
stable = (df['Status'] == "Stable").sum()
moderate = (df['Status'] == "Moderate").sum()
critical = (df['Status'] == "Critical").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", total_patients)
col2.metric("Stable", stable)
col3.metric("Moderate", moderate)
col4.metric("Critical", critical)

# -----------------------------
# Alerts (Professional Style)
# -----------------------------
st.subheader("🚨 Alerts & Recommendations")

if critical > 0:
    st.error(f"🛑 {critical} Patient(s) in CRITICAL condition! \n\n"
             f"➡ Immediate medical intervention required.\n"
             f"➡ Review vitals and prioritize triage.")
if moderate > 0:
    st.warning(f"⚠️ {moderate} Patient(s) in MODERATE condition. \n\n"
               f"➡ Continuous monitoring recommended.\n"
               f"➡ Escalate if vitals deteriorate.")
if stable > 0:
    st.success(f"✅ {stable} Patient(s) are currently Stable. \n\n"
               f"➡ No urgent action needed.\n"
               f"➡ Continue routine monitoring.")

# -----------------------------
# Patient Table
# -----------------------------
st.subheader("📋 Patient Risk Overview")
st.dataframe(df[['Patient_ID','HR','SpO₂','Temp','RR','RiskScore','Status']])

# -----------------------------
# Vital Trends
# -----------------------------
st.subheader("📈 Vital Signs Trends")

# Line chart trends (requires PatientID to simulate over time)
fig_hr = px.line(df, x="Patient_ID", y="HR", color="Status", markers=True, title="Heart Rate Trend")
fig_spo2 = px.line(df, x="Patient_ID", y="SpO₂", color="Status", markers=True, title="SpO₂ Trend")
fig_temp = px.line(df, x="Patient_ID", y="Temp", color="Status", markers=True, title="Temperature Trend")
fig_rr = px.line(df, x="Patient_ID", y="RR", color="Status", markers=True, title="Respiratory Rate Trend")

st.plotly_chart(fig_hr, use_container_width=True)
st.plotly_chart(fig_spo2, use_container_width=True)
st.plotly_chart(fig_temp, use_container_width=True)
st.plotly_chart(fig_rr, use_container_width=True)

# -----------------------------
# Risk Distribution
# -----------------------------
st.subheader("📊 Risk Distribution Overview")
fig_pie = px.pie(df, names="Status", title="Patient Risk Category Distribution")
st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------
# Automated Suggestions
# -----------------------------
st.subheader("💡 AI-Based Suggestions")

for idx, row in df.iterrows():
    if row['Status'] == "Critical":
        st.error(f"Patient {row['Patient_ID']} → CRITICAL ⚠️ \n"
                 f"👉 Suggestion: Immediate doctor review required. Consider oxygen support or ICU transfer.")
    elif row['Status'] == "Moderate":
        st.warning(f"Patient {row['Patient_ID']} → MODERATE ⚠️ \n"
                   f"👉 Suggestion: Monitor every 30 mins. Schedule physician check-up.")
    else:
        st.success(f"Patient {row['Patient_ID']} → Stable ✅ \n"
                   f"👉 Suggestion: Routine monitoring only.")
