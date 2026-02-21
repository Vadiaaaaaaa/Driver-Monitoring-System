import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Driver Monitoring Dashboard",
    layout="wide"
)

st.title("🚗 AI Driver Monitoring – Fleet Analytics")

DATA_PATH = "data/session_logs.csv"

# -----------------------------
# Load Data Safely
# -----------------------------
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error("No session data found or file cannot be read.")
    st.stop()

if df.empty:
    st.warning("Session log file is empty.")
    st.stop()

# -----------------------------
# Safe Timestamp Conversion
# -----------------------------
if "timestamp" not in df.columns:
    st.error("Timestamp column missing in CSV.")
    st.stop()

df["timestamp"] = (
    df["timestamp"]
    .astype(str)
    .str.strip()
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    format="ISO8601"
)

# Drop invalid timestamps
df = df.dropna(subset=["timestamp"])

# Sort for clean plotting
df = df.sort_values("timestamp")

if df.empty:
    st.error("No valid timestamp records found after parsing.")
    st.stop()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

device_ids = df["device_id"].unique()
selected_device = st.sidebar.selectbox("Select Device", device_ids)

df = df[df["device_id"] == selected_device]

session_ids = df["session_id"].unique()
selected_session = st.sidebar.selectbox("Select Session", session_ids)

df = df[df["session_id"] == selected_session]

if df.empty:
    st.warning("No data available for selected device/session.")
    st.stop()

# -----------------------------
# KPI Row
# -----------------------------
avg_risk = df["risk_score"].mean()
max_risk = df["risk_score"].max()
avg_blink = df["blink_rate"].mean()
total_records = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Risk", f"{avg_risk:.2f}")
col2.metric("Max Risk", f"{max_risk:.2f}")
col3.metric("Avg Blink Rate", f"{avg_blink:.1f} /min")
col4.metric("Total Records", total_records)

st.divider()

# -----------------------------
# 2x2 Analytics Grid
# -----------------------------
colA, colB = st.columns(2)

# Risk Over Time
with colA:
    st.subheader("Risk Score Over Time")
    fig1, ax1 = plt.subplots()
    ax1.plot(df["timestamp"], df["risk_score"])
    ax1.set_ylim(0, 1)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Risk Score")
    st.pyplot(fig1)

# Blink Rate
with colB:
    st.subheader("Blink Rate Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df["timestamp"], df["blink_rate"])
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Blink Rate (/min)")
    st.pyplot(fig2)

colC, colD = st.columns(2)

# Head Yaw Distribution
with colC:
    st.subheader("Head Yaw Distribution")
    fig3, ax3 = plt.subplots()
    ax3.hist(df["yaw"], bins=30)
    ax3.set_xlabel("Yaw Angle")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

# Driver State Distribution
with colD:
    st.subheader("Driver State Distribution")
    state_counts = df["state"].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.pie(state_counts, labels=state_counts.index, autopct="%1.1f%%")
    st.pyplot(fig4)
