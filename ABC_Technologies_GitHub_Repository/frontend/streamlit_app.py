import streamlit as st
import requests
import os

st.set_page_config(
    page_title="ABC Technologies AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ABC Technologies")
st.caption("Enterprise AI Assistant | Intelligent Business Operations")

# Configuration
try:
    API_URL = st.secrets["API_URL"].rstrip("/")
    API_KEY = st.secrets["API_KEY"]
except Exception:
    API_URL = os.getenv("API_URL", "").rstrip("/")
    API_KEY = os.getenv("API_KEY", "")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Dashboard", "Policy Assistant", "Order Calculator"]
)

st.sidebar.divider()
st.sidebar.caption("Powered by Qwen, LangGraph, RAG and MCP")

if page == "Dashboard":

    st.subheader("Enterprise Operations Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("AI Platform", "Active Prototype")
    c2.metric("Knowledge Base", "FAISS + RAG")
    c3.metric("Business Tools", "MCP")

    st.info(
        "Welcome to ABC Technologies Enterprise AI. "
        "Use the navigation menu to access company policies "
        "or calculate customer orders."
    )

elif page == "Policy Assistant":

    st.subheader("Customer Policy Assistant")

    customer_id = st.selectbox(
        "Customer",
        ["customer_001", "customer_002"]
    )

    question = st.text_area(
        "Ask a company policy question",
        placeholder="How many days do I have to request a refund?"
    )

    if st.button("Ask Enterprise AI", type="primary"):

        if not API_URL or not API_KEY:
            st.error("Configure API_URL and API_KEY in app secrets.")
        elif not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Enterprise AI is processing..."):
                    response = requests.post(
                        API_URL + "/api/assistant",
                        headers={"X-API-Key": API_KEY},
                        json={
                            "customer_id": customer_id,
                            "intent": "question",
                            "question": question
                        },
                        timeout=180
                    )

                response.raise_for_status()
                data = response.json()

                st.success("Answer generated successfully")
                st.write(data.get("answer", "No answer returned"))

                with st.expander("Sources"):
                    st.write(data.get("sources", []))

            except Exception as e:
                st.error(f"Request failed: {e}")

elif page == "Order Calculator":

    st.subheader("Business Order Calculator")

    customer_id = st.selectbox(
        "Customer",
        ["customer_001", "customer_002"],
        key="order_customer"
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=8
    )

    unit_price = st.number_input(
        "Unit price",
        min_value=0.0,
        value=350.0
    )

    if st.button("Calculate Order", type="primary"):

        if not API_URL or not API_KEY:
            st.error("Configure API_URL and API_KEY in app secrets.")
        else:
            try:
                with st.spinner("Executing MCP business tool..."):
                    response = requests.post(
                        API_URL + "/api/assistant",
                        headers={"X-API-Key": API_KEY},
                        json={
                            "customer_id": customer_id,
                            "intent": "calculate",
                            "quantity": quantity,
                            "unit_price": unit_price
                        },
                        timeout=180
                    )

                response.raise_for_status()
                data = response.json()

                st.success("MCP calculation successful")
                st.metric(
                    "Verified Order Total",
                    f'{data["currency"]} {data["total"]:,.2f}'
                )

                st.write("Customer:", data["customer"])
                st.write("Tool:", data["tool"])

            except Exception as e:
                st.error(f"Request failed: {e}")

st.divider()
st.caption("ABC Technologies | Enterprise AI Capstone Project")
