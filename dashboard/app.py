import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

st.set_page_config(page_title="Driver Monitoring Dashboard", layout="wide")

st.title("AI Driver Monitoring – Cloud Analytics")

API_URL = "http://127.0.0.1:8000/metrics"

# -----------------------------
# Fetch Data From Backend
# -----------------------------
try:
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data)
except:
    st.error("Backend not reachable. Is FastAPI running?")
    st.stop()

if df.empty:
    st.warning("No metrics available in database.")
    st.stop()

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------------
# Summary Metrics Row
# -----------------------------
colA, colB, colC, colD = st.columns(4)

colA.metric("Average Risk", f"{df['risk_score'].mean():.2f}")
colB.metric("Max Risk", f"{df['risk_score'].max():.2f}")
colC.metric("Avg Blink Rate", f"{df['blink_rate'].mean():.1f}/min")
colD.metric("Total Records", len(df))

st.divider()

# -----------------------------
# 2 x 2 Layout
# -----------------------------
col1, col2 = st.columns(2)

# ---- Risk Over Time ----
with col1:
    st.subheader("Risk Score Over Time")
    fig1, ax1 = plt.subplots()
    ax1.plot(df["timestamp"], df["risk_score"])
    ax1.set_ylim(0, 1)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Risk Score")
    st.pyplot(fig1)

# ---- Blink Rate ----
with col2:
    st.subheader("Blink Rate Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df["timestamp"], df["blink_rate"])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Blink Rate (/min)")
    st.pyplot(fig2)

col3, col4 = st.columns(2)

# ---- Yaw Distribution ----
with col3:
    st.subheader("Head Yaw Distribution")
    fig3, ax3 = plt.subplots()
    ax3.hist(df["yaw"], bins=30)
    ax3.set_xlabel("Yaw Angle")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

# ---- State Distribution ----
with col4:
    st.subheader("Driver State Distribution")
    state_counts = df["state"].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.pie(state_counts, labels=state_counts.index, autopct="%1.1f%%")
    st.pyplot(fig4)
