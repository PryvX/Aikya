import streamlit as st
import pandas as pd
import subprocess
import os
import signal

df = pd.read_csv("data/AA2.csv")

st.title("🏦 Account Aggregator 2")

st.subheader("📄 Financial Request Data")
st.dataframe(df)

# Store process ID in session state
if "api_process" not in st.session_state:
    st.session_state.api_process = None

st.subheader("⚙️ API Controls")

col1, col2 = st.columns(2)

# Start API
with col1:
    if st.button("▶️ Start API Server"):
        if st.session_state.api_process is None:
            process = subprocess.Popen(
                ["python", "-m", "uvicorn", "lender2:app", "--host", "0.0.0.0", "--port", "8002"]
            )
            st.session_state.api_process = process
            st.success("✅ API Server started on port 8002")
        else:
            st.warning("API server is already running.")

# Stop API
with col2:
    if st.button("⏹️ Stop API Server"):
        if st.session_state.api_process:
            os.kill(st.session_state.api_process.pid, signal.SIGTERM)
            st.session_state.api_process = None
            st.success("🛑 API Server stopped.")
        else:
            st.warning("API server is not running.")
