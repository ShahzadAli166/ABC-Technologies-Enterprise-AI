import os
import requests
import streamlit as st

# ABC Technologies — Enterprise AI Dashboard v2
# Frontend: Streamlit | API: Cloudflare Workers | Data: D1 | Inference: Workers AI

st.set_page_config(
    page_title="ABC Technologies | Enterprise AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------
# VISUAL DESIGN
# -------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background: #F3F6FA; }
    .block-container { max-width: 1380px; padding-top: 1.8rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: #102A43; border-right: 1px solid #24445F; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span { color: #EAF2F8; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #FFFFFF; }
    [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #DFE7F0;
        border-radius: 14px; padding: 16px 18px;
        box-shadow: 0 3px 12px rgba(16,42,67,.045);
    }
    [data-testid="stMetricLabel"] { color: #52677D; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #102A43; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px; border-color: #DFE7F0; background: #FFFFFF;
    }
    [data-testid="stChatMessage"] {
        background: #FFFFFF; border: 1px solid #DFE7F0;
        border-radius: 14px; padding: 12px 16px; margin-bottom: 10px;
    }
    .hero {
        background: linear-gradient(115deg, #102A43 0%, #174B68 62%, #0F766E 100%);
        padding: 27px 31px; border-radius: 19px; color: #FFFFFF;
        margin-bottom: 22px; box-shadow: 0 8px 24px rgba(16,42,67,.13);
    }
    .hero-kicker { color: #99F6E4; font-size: .74rem; font-weight: 800;
        letter-spacing: .13em; text-transform: uppercase; margin-bottom: 9px; }
    .hero h1 { color: #FFFFFF !important; font-size: 2.05rem;
        margin: 0 0 8px 0; line-height: 1.2; }
    .hero p { color: #E0EDF5; font-size: 1rem; margin: 0; }
    .section-kicker { color: #0F766E; text-transform: uppercase;
        letter-spacing: .1em; font-size: .72rem; font-weight: 800; margin-bottom: 4px; }
    .soft-note { background: #E5F3F2; border-left: 4px solid #0F766E;
        padding: 13px 16px; border-radius: 8px; color: #164E52; margin: 10px 0 18px 0; }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #0F766E; border: 1px solid #0F766E; color: #FFFFFF;
        border-radius: 9px; font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #115E59; border-color: #115E59; color: #FFFFFF;
    }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# CONFIGURATION AND API CLIENT
# -------------------------------------------------------------------
try:
    API_URL = st.secrets["API_URL"].rstrip("/")
    API_KEY = st.secrets["API_KEY"]
except Exception:
    API_URL = os.getenv("API_URL", "").rstrip("/")
    API_KEY = os.getenv("API_KEY", "")

WORKER_URL = f"{API_URL}/api/assistant" if API_URL else ""


def call_assistant(payload):
    """Call the existing authenticated Cloudflare Worker API."""
    if not API_URL or not API_KEY:
        raise RuntimeError("API_URL or API_KEY is missing. Configure both in Streamlit Secrets.")

    response = requests.post(
        WORKER_URL,
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )

    try:
        data = response.json()
    except ValueError:
        data = {"error": "The API returned a non-JSON response."}

    if not response.ok:
        raise RuntimeError(
            f"API request failed ({response.status_code}): {data.get('error', 'Unknown error')}"
        )
    return data


def get_health():
    if not API_URL:
        raise RuntimeError("API_URL is missing from Streamlit Secrets.")
    response = requests.get(f"{API_URL}/health", timeout=30)
    response.raise_for_status()
    return response.json()


def show_hero(kicker, title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-kicker">{kicker}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("# 🤖 ABC")
    st.markdown("### Technologies")
    st.caption("ENTERPRISE INTELLIGENCE")
    st.divider()
    page = st.radio(
        "WORKSPACE",
        ["Overview", "Policy Assistant", "Order Calculator"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("**PLATFORM**")
    st.caption("✦ Cloudflare Workers AI")
    st.caption("▦ Cloudflare D1 Database")
    st.caption("◇ Authenticated API Gateway")
    st.divider()
    st.caption("ABC Technologies")
    st.caption("Enterprise AI Demonstration")


# ===================================================================
# 1. OVERVIEW — METRICS, PLATFORM STATUS, WORKFLOW CARDS
# ===================================================================
if page == "Overview":
    show_hero(
        "ENTERPRISE INTELLIGENCE PLATFORM",
        "Business operations, made smarter.",
        "A unified workspace for company knowledge, customer support and order calculations.",
    )

    st.markdown('<div class="section-kicker">SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
    st.subheader("Your AI operations at a glance")

    c1, c2, c3 = st.columns(3, gap="medium")
    c1.metric("AI inference", "Workers AI", "GLM-4.7-Flash")
    c2.metric("Knowledge store", "Cloudflare D1", "3 policy records")
    c3.metric("API gateway", "Cloudflare", "Authenticated")

    st.write("")
    left, right = st.columns([1.35, 1], gap="large")

    with left:
        with st.container(border=True):
            st.markdown("### 👋 Welcome to ABC Technologies")
            st.write(
                "Use the workspace to retrieve information from company policies "
                "or calculate customer orders through the connected business API."
            )
            st.markdown(
                '<div class="soft-note"><b>Available workflows</b><br>'
                'Policy questions grounded in company records · Customer-aware responses · '
                'Validated order calculations</div>',
                unsafe_allow_html=True,
            )
            a, b = st.columns(2)
            with a:
                st.write("**📚 Policy Assistant**")
                st.caption("Ask about refunds, processing and support.")
            with b:
                st.write("**🧮 Order Calculator**")
                st.caption("Calculate customer order totals.")

    with right:
        with st.container(border=True):
            st.markdown("### ☁️ Live service status")
            st.write("Check the deployed gateway and its database connection.")
            if st.button("Check live system", type="primary", use_container_width=True):
                try:
                    with st.spinner("Checking Cloudflare services..."):
                        health = get_health()
                    if health.get("status") == "healthy":
                        st.success("Cloudflare Worker is healthy.")
                    else:
                        st.warning("The service reported a degraded status.")
                    st.json(health)
                except Exception as exc:
                    st.error(str(exc))

    st.caption("Deployment: Streamlit Community Cloud · Cloudflare Workers · Workers AI · D1")


# ===================================================================
# 2. POLICY ASSISTANT — CHAT UI, CUSTOMER PROFILE, SOURCES
# ===================================================================
elif page == "Policy Assistant":
    show_hero(
        "CUSTOMER KNOWLEDGE",
        "Policy Assistant",
        "Ask a question about company policies and receive an AI-generated response grounded in company records.",
    )

    col_main, col_profile = st.columns([2.1, 1], gap="large")

    with col_profile:
        with st.container(border=True):
            st.markdown("### 👤 Customer profile")
            customer_id = st.selectbox(
                "Choose demo customer",
                ["customer_001", "customer_002"],
                format_func=lambda x: "Ahmed · PKR" if x == "customer_001" else "Sara · USD",
                key="policy_customer",
            )
            if customer_id == "customer_001":
                st.markdown("**Ahmed**")
                st.caption("Preferred currency: PKR")
                st.caption("Preferred contact: Email")
            else:
                st.markdown("**Sara**")
                st.caption("Preferred currency: USD")
                st.caption("Preferred contact: Email")

            st.divider()
            st.markdown("**Knowledge topics**")
            st.caption("• Refund policy")
            st.caption("• Order processing")
            st.caption("• Customer support")

            if st.button("Clear this chat", use_container_width=True):
                st.session_state[f"policy_history_{customer_id}"] = []
                st.rerun()

    with col_main:
        with st.container(border=True):
            st.markdown("### 💬 Ask your company-policy question")
            st.caption("Answers are generated using the company's stored policy records.")

            history_key = f"policy_history_{customer_id}"
            if history_key not in st.session_state:
                st.session_state[history_key] = []

            for item in st.session_state[history_key]:
                with st.chat_message(
                    item["role"],
                    avatar="👤" if item["role"] == "user" else "🤖",
                ):
                    st.markdown(item["content"])
                    if item.get("sources"):
                        with st.expander("View source documents"):
                            for source in item["sources"]:
                                st.caption(f"📄 {source}")
                    if item.get("model"):
                        st.caption(f"Model: {item['model']}")

            prompt = st.chat_input(
                "Ask about refunds, order processing or support...",
                key=f"policy_chat_input_{customer_id}",
            )

            if prompt:
                st.session_state[history_key].append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)

                with st.chat_message("assistant", avatar="🤖"):
                    try:
                        with st.spinner("Searching company records and generating an answer..."):
                            result = call_assistant({
                                "customer_id": customer_id,
                                "intent": "question",
                                "question": prompt,
                            })

                        answer = result.get("answer", "No answer was returned.")
                        st.markdown(answer)
                        sources = result.get("sources", [])

                        if sources:
                            with st.expander("View source documents"):
                                for source in sources:
                                    st.caption(f"📄 {source}")

                        model_name = result.get("model", "Cloudflare Workers AI")
                        st.caption(f"Generated by {model_name}")
                        st.session_state[history_key].append({
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                            "model": model_name,
                        })
                    except Exception as exc:
                        st.error(str(exc))
                        st.session_state[history_key].append({
                            "role": "assistant",
                            "content": f"Request failed: {exc}",
                        })


# ===================================================================
# 3. ORDER CALCULATOR — CUSTOMER FORM, RESULT CARD, BREAKDOWN
# ===================================================================
elif page == "Order Calculator":
    show_hero(
        "BUSINESS OPERATIONS",
        "Order Calculator",
        "Prepare an order, validate the inputs and calculate the total through the live Cloudflare business API.",
    )

    input_col, result_col = st.columns([1.2, 1], gap="large")

    with input_col:
        with st.container(border=True):
            st.markdown("### 🧾 Order details")
            st.caption("Enter the customer and order information.")

            with st.form("order_calculator_form", border=False):
                customer_id = st.selectbox(
                    "Customer",
                    ["customer_001", "customer_002"],
                    format_func=lambda x: "Ahmed · PKR" if x == "customer_001" else "Sara · USD",
                )
                default_price = 350.0 if customer_id == "customer_001" else 50.0
                quantity = st.number_input(
                    "Quantity", min_value=1, max_value=100000, value=8, step=1
                )
                unit_price = st.number_input(
                    "Unit price", min_value=0.0, max_value=1000000000.0,
                    value=default_price, step=50.0 if customer_id == "customer_001" else 5.0,
                )
                submitted = st.form_submit_button(
                    "Calculate order total", type="primary", use_container_width=True
                )

    with result_col:
        with st.container(border=True):
            st.markdown("### 📊 Calculation result")
            st.caption("Your verified order summary will appear here.")

            if submitted:
                try:
                    with st.spinner("Calculating order through Cloudflare..."):
                        result = call_assistant({
                            "customer_id": customer_id,
                            "intent": "calculate",
                            "quantity": int(quantity),
                            "unit_price": float(unit_price),
                        })

                    currency = result["currency"]
                    total = result["total"]
                    st.success("Order calculation completed")
                    st.metric("Total order amount", f"{currency} {total:,.2f}")
                    st.divider()
                    st.write(f"**Customer:** {result['customer']}")
                    st.write(f"**Quantity:** {result['quantity']:,}")
                    st.write(f"**Unit price:** {currency} {result['unit_price']:,.2f}")
                    st.write(f"**Execution:** {result.get('execution', 'Cloudflare Worker')}")
                    st.markdown(
                        '<div class="soft-note"><b>Calculation verified</b><br>'
                        'The total was returned by the deployed business API.</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as exc:
                    st.error(str(exc))
            else:
                st.info("Complete the order details and calculate to see the result.")
                st.markdown("**Calculation formula**")
                st.latex(r"\text{Order Total} = \text{Quantity} \times \text{Unit Price}")


# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------
st.divider()
st.caption("ABC Technologies · Enterprise AI Demonstration · Streamlit + Cloudflare Workers AI + D1")
