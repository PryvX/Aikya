import streamlit as st
import requests
import hashlib

def hash_value(val):
    return hashlib.sha256(val.encode()).hexdigest()

# Simulated lender node endpoints
LENDER_NODES = {
    "Account Aggregator 1": "http://localhost:8001",
    "Account Aggregator 2": "http://localhost:8002",
    "Account Aggregator 3": "http://localhost:8003",
}

logo_image = "sahamati.png"
st.image(logo_image, width=200)

st.title("Sahamati Federated Orchestrator")

st.sidebar.header("Choose Federated Query")

query_type = st.sidebar.selectbox("Query Type", ["Identity Mismatch Detection", "Identity Reuse Detection", 
                                                 "Loan Inquiry Velocity Check"])

if 'results' not in st.session_state:
    st.session_state.results = {}

if query_type == "Identity Mismatch Detection":
    pan_id = st.text_input("Enter PAN ID", "ETFZT6789C")
    aadhaar_id = st.text_input("Enter Adhaar ID", "213508980534")
    full_name = st.text_input("Enter Full name", value="Ravi Kumar")
    
    if st.button("Run Federated Query"):
        st.markdown(f"🔐 **Encrypted Pan + Aadhaar + Full_name:** `{hash_value(aadhaar_id)}`")
        temp_results = {}

        for lender_name, lender_url in LENDER_NODES.items():
            try:
                st.markdown(f"📡 **Sending Query to:** `{lender_name}`")
                response = requests.post(
                    f"{lender_url}/query/identity_mismatch",
                    json={"pan": pan_id,
                          "aadhaar": aadhaar_id,
                          "name": full_name},
                    timeout=5
                )
                result = response.json()
            except Exception as e:
                result = {"error": str(e)}

            temp_results[lender_name] = result
        st.session_state.results = temp_results

elif query_type == "Identity Reuse Detection":
    pan_id = st.text_input("Enter PAN ID", "ETFZT1234C")
    aadhaar_id = st.text_input("Enter Adhaar ID", "598508980534")
    full_name = st.text_input("Enter Full name", value="Nitesh Sharma")

    identity_hash = hash_value(pan_id+"_"+aadhaar_id+"_"+full_name)
    
    if st.button("Run Federated Query"):
        st.markdown(f"🔐 **Encrypted Pan + Aadhaar + Full_name:** `{hash_value(identity_hash)}`")
        temp_results = {}

        for lender_name, lender_url in LENDER_NODES.items():
            try:
                st.markdown(f"📡 **Sending Query to:** `{lender_name}`")
                response = requests.post(
                    f"{lender_url}/query/identity_hash_reuse",
                    json={"identity_hash": identity_hash},
                    timeout=5
                )
                result = response.json()
            except Exception as e:
                result = {"error": str(e)}

            temp_results[lender_name] = result
        st.session_state.results = temp_results

elif query_type == "Loan Inquiry Velocity Check":
    phone_number = st.text_input("Enter Phone Number", "9805456733")
    purpose_code = st.text_input("Enter Purpose Code", "103")
    past_days = st.text_input("Enter Past X Days", "15")
    phone_hash = hash_value(phone_number)
    
    if st.button("Run Federated Query"):
        st.markdown(f"🔐 **Encrypted Phone Number:** `{phone_hash}`")
        temp_results = {}

        for lender_name, lender_url in LENDER_NODES.items():
            try:
                st.markdown(f"📡 **Sending Query to:** `{lender_name}`")
                response = requests.post(
                    f"{lender_url}/query/aa_velocity_check",
                    json={"phone_hash": phone_hash},
                    timeout=5
                )
                result = response.json()
            except Exception as e:
                result = {"error": str(e)}

            temp_results[lender_name] = result
        st.session_state.results = temp_results


aggregate_pull_count = 0
aggregate_unique_fiu_count = 0

if st.session_state.results:
    st.subheader("Federated Results")
    for lender_name, result in st.session_state.results.items():
        st.write(f"### {lender_name}")
        st.json(result)
        aggregate_pull_count += result["pulled_record_count"]
    st.warning("Risk Score: High")
    st.warning(f"Aggregate pull count: {aggregate_pull_count}")
