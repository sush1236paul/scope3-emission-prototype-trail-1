import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Scope-3 Auditor", layout="wide")
st.title("🌱 Scope-3 Supply Chain Auditor")

# -----------------------------
# Upload Section
# -----------------------------
st.header("Upload Document")

batch_name = st.text_input("Current Batch Name", value="Batch-01")
uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "png", "jpg", "txt"])

if uploaded_file and st.button("Run Audit"):
    with st.spinner("Processing..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        params = {"batch_name": batch_name}

        try:
            res = requests.post(
                f"{BACKEND_URL}/process",
                files=files,
                params=params
            )
            result = res.json()

            st.success("Document processed successfully")
            st.metric("Estimated CO₂e", f"{result['total_emissions_kgco2e']} kg")
            st.info(f"Evidence: {result['extracted_data']['evidence']}")

        except Exception as e:
            st.error(f"Error: {e}")

# -----------------------------
# History & Comparison Section
# -----------------------------
st.divider()
st.header("Batch Comparison & History")

history_response = requests.get(f"{BACKEND_URL}/history")

if history_response.status_code == 200 and history_response.json():
    df = pd.DataFrame(history_response.json())

    # -----------------------------
    # Batch Comparison (Manual)
    # -----------------------------
    st.subheader("Batch Comparison")

    batches = df["batch"].unique().tolist()

    if len(batches) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            batch_a = st.selectbox("Select Batch A", batches, key="batch_a")

        with col2:
            batch_b = st.selectbox("Select Batch B", batches, key="batch_b")

        if batch_a != batch_b:
            total_a = df[df["batch"] == batch_a]["total_emissions_kgco2e"].sum()
            total_b = df[df["batch"] == batch_b]["total_emissions_kgco2e"].sum()
            diff = round(total_b - total_a, 2)

            st.metric(f"{batch_a} Total", f"{total_a} kg CO₂e")
            st.metric(f"{batch_b} Total", f"{total_b} kg CO₂e")

            if diff > 0:
                st.warning(f"Emissions increased by {diff} kg CO₂e")
            elif diff < 0:
                st.success(f"Emissions reduced by {abs(diff)} kg CO₂e")
            else:
                st.info("No change in emissions")
    else:
        st.info("Upload at least two batches to compare.")

    # -----------------------------
    # Audit History Table
    # -----------------------------
    st.subheader("Audit History")
    st.dataframe(
        df[["timestamp", "supplier", "batch", "total_emissions_kgco2e"]],
        use_container_width=True
    )
else:
    st.info("No history available yet. Upload documents to begin.")
