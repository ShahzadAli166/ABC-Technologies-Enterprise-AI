
# ABC Technologies — Live Enterprise AI Dashboard
# Streamlit + Cloudflare Workers AI + D1

import streamlit as st
import requests

st.set_page_config(
    page_title="ABC Technologies Enterprise AI",
    page_icon="🤖",
    layout="wide"
)

# 1. Load secure application secrets
try:
    API_URL = st.secrets["API_URL"].rstrip("/")
    API_KEY = st.secrets["API_KEY"]
except Exception:
    API_URL = ""
    API_KEY = ""

WORKER_URL = API_URL + "/api/assistant" if API_URL else ""

# 2. API communication
def api_request(payload):

    if not API_URL or not API_KEY:
        raise ValueError("API_URL or API_KEY is not configured.")

    response = requests.post(
        WORKER_URL,
        headers={"X-API-Key": API_KEY},
        json=payload,
        timeout=120
    )

    if not response.ok:
        try:
            detail = response.json().get("error", "Request failed")
        except Exception:
            detail = "Request failed"

        raise RuntimeError(f"HTTP {response.status_code}: {detail}")

    return response.json()


# 3. Dashboard header
st.title("🤖 ABC Technologies")
st.caption("Enterprise AI Assistant | Intelligent Business Operations")

# 4. Navigation
st.sidebar.title("ABC Technologies")
page = st.sidebar.radio(
    "Choose Module",
    ["Overview", "Policy Assistant", "Order Calculator"]
)

st.sidebar.divider()
st.sidebar.caption("Powered by Cloudflare Workers AI")
st.sidebar.caption("Database: Cloudflare D1")

# 5. Overview
if page == "Overview":

    st.subheader("Enterprise Operations Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("AI Inference", "Workers AI")
    col2.metric("Company Database", "D1")
    col3.metric("API Gateway", "Cloudflare")

    if st.button("Check Live System Status"):

        try:
            response = requests.get(
                API_URL + "/health",
                timeout=30
            )

            response.raise_for_status()
            data = response.json()

            st.success("Enterprise AI system is healthy!")
            st.json(data)

        except Exception as error:
            st.error(f"Health check failed: {error}")

    st.info(
        "Welcome to ABC Technologies. "
        "Use the navigation menu to ask company policy "
        "questions or calculate customer orders."
    )

# 6. Policy Assistant
elif page == "Policy Assistant":

    st.subheader("📚 Customer Policy Assistant")

    customer_id = st.selectbox(
        "Select Customer",
        ["customer_001", "customer_002"]
    )

    question = st.text_area(
        "Ask a company policy question",
        placeholder="How many days do I have to request a refund?"
    )

    if st.button("Ask Enterprise AI", type="primary"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:
            try:
                with st.spinner("Searching company knowledge and generating answer..."):

                    data = api_request({
                        "customer_id": customer_id,
                        "intent": "question",
                        "question": question
                    })

                st.success("Answer generated successfully!")

                st.markdown("### AI Response")
                st.write(data["answer"])

                st.markdown("### Customer")
                st.write(data["customer"])

                with st.expander("View document sources"):
                    st.write(data.get("sources", []))

                st.caption(
                    "Model: " + data.get("model", "Workers AI")
                )

            except Exception as error:
                st.error(str(error))

# 7. Order Calculator
elif page == "Order Calculator":

    st.subheader("🧮 Business Order Calculator")

    customer_id = st.selectbox(
        "Select Customer",
        ["customer_001", "customer_002"],
        key="order_customer"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=100000,
        value=8,
        step=1
    )

    unit_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        value=350.0,
        step=50.0
    )

    if st.button("Calculate Order", type="primary"):

        try:
            with st.spinner("Calculating order..."):

                data = api_request({
                    "customer_id": customer_id,
                    "intent": "calculate",
                    "quantity": int(quantity),
                    "unit_price": float(unit_price)
                })

            st.success("Order calculation successful!")

            st.metric(
                "Total Order Amount",
                f'{data["currency"]} {data["total"]:,.2f}'
            )

            col1, col2 = st.columns(2)

            col1.write("Customer: " + data["customer"])
            col1.write("Quantity: " + str(data["quantity"]))

            col2.write("Unit price: " + str(data["unit_price"]))
            col2.write("Execution: " + data["execution"])

        except Exception as error:
            st.error(str(error))

# 8. Footer
st.divider()
st.caption("ABC Technologies | Enterprise AI Capstone")
