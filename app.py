import streamlit as st
import pandas as pd
import plotly.express as px

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
    condition_cols = [c for c in df.columns if c not in ['PatientID','HR','SpO₂','Temp','RR']]
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
# Alerts
# -----------------------------
st.subheader("🚨 Alerts")
if critical > 0:
    st.error(f"⚠️ {critical} patients in CRITICAL condition! Immediate action required.")
if moderate > 0:
    st.warning(f"⚠️ {moderate} patients in MODERATE condition. Please review.")

# -----------------------------
# Patient Table
# -----------------------------
st.subheader("📋 Patient Risk Overview")
st.dataframe(df[['Patient_ID','HR','SpO₂','Temp','RR','RiskScore','Status']])

# -----------------------------
# Visualizations
# -----------------------------
st.subheader("📈 Vitals Trends")
fig_pie = px.pie(df, names="Status", title="Risk Category Distribution")
st.plotly_chart(fig_pie, use_container_width=True)
