import os
import requests
import streamlit as st

# =========================================================
# ABC TECHNOLOGIES — ENTERPRISE AI DASHBOARD V2
# Streamlit + Cloudflare Workers AI + Cloudflare D1
# =========================================================

st.set_page_config(
    page_title="ABC Technologies | Enterprise AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Visual identity and styling
# -------------------------
st.markdown(
    """
    <style>
    .stApp { background: #F3F6FA; }
    .block-container {
        max-width: 1380px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    [data-testid="stSidebar"] {
        background: #102A43;
        border-right: 1px solid #24445F;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span { color: #EAF2F8; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #FFFFFF; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #DFE7F0;
        border-radius: 14px;
        padding: 17px 18px;
        box-shadow: 0 3px 12px rgba(16,42,67,0.045);
    }
    [data-testid="stMetricLabel"] { color: #52677D; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #102A43; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        border-color: #DFE7F0;
        background: #FFFFFF;
    }
    [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #DFE7F0;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .hero {
        background: linear-gradient(115deg, #102A43 0%, #174B68 62%, #0F766E 100%);
        padding: 28px 32px;
        border-radius: 20px;
        color: #FFFFFF;
        margin-bottom: 22px;
        box-shadow: 0 8px 24px rgba(16,42,67,0.13);
    }
    .hero-kicker {
        color: #99F6E4;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }
    .hero h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero p { color: #E0EDF5; font-size: 1rem; margin: 0; }
    .section-kicker {
        color: #0F766E;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .soft-note {
        background: #E5F3F2;
        border-left: 4px solid #0F766E;
        padding: 13px 16px;
        border-radius: 8px;
        color: #164E52;
        margin: 10px 0 18px 0;
    }
    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: #0F766E;
        border: 1px solid #0F766E;
        color: white;
        border-radius: 9px;
        font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stFormSubmitButton > button[kind="primary"]:hover {
        background: #115E59;
        border-color: #115E59;
        color: white;
    }
    div.stButton > button {
        border-radius: 9px;
    }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Secure API configuration
# -------------------------
try:
    API_URL = st.secrets["API_URL"].rstrip("/")
    API_KEY = st.secrets["API_KEY"]
except Exception:
    API_URL = os.getenv("API_URL", "").rstrip("/")
    API_KEY = os.getenv("API_KEY", "")

WORKER_URL = f"{API_URL}/api/assistant" if API_URL else ""


def call_assistant(payload: dict) -> dict:
    """Call the existing authenticated Cloudflare Worker API."""
    if not API_URL or not API_KEY:
        raise RuntimeError(
            "API_URL or API_KEY is missing. Configure both in Streamlit Secrets."
        )

    response = requests.post(
        WORKER_URL,
        headers={
            "X-API-Key": API_KEY,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=120,
    )

    try:
        data = response.json()
    except ValueError:
        data = {"error": "The API returned a non-JSON response."}

    if not response.ok:
        raise RuntimeError(
            f"API request failed ({response.status_code}): "
            f"{data.get('error', 'Unknown error')}"
        )
    return data


def get_health() -> dict:
    if not API_URL:
        raise RuntimeError("API_URL is missing from Streamlit Secrets.")
    response = requests.get(f"{API_URL}/health", timeout=30)
    response.raise_for_status()
    return response.json()


def show_hero(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{kicker}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def customer_label(customer_id: str) -> str:
    return "Ahmed · PKR" if customer_id == "customer_001" else "Sara · USD"


def render_chat_history(history: list) -> None:
    for item in history:
        avatar = "👤" if item.get("role") == "user" else "🤖"
        with st.chat_message(item.get("role", "assistant"), avatar=avatar):
            st.markdown(item.get("content", ""))
            if item.get("sources"):
                with st.expander("View source documents"):
                    for source in item["sources"]:
                        st.caption(f"📄 {source}")
            if item.get("model"):
                st.caption(f"Generated by {item['model']}")


def answer_policy_question(customer_id: str, prompt: str, history_key: str) -> None:
    """Submit a question, display the answer and retain session chat history."""
    st.session_state[history_key].append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        try:
            with st.spinner("ABC AI is checking company records..."):
                result = call_assistant({
                    "customer_id": customer_id,
                    "intent": "question",
                    "question": prompt,
                })

            answer = result.get("answer", "No answer was returned.")
            sources = result.get("sources", [])
            model_name = result.get("model", "Cloudflare Workers AI")

            st.markdown(answer)
            if sources:
                with st.expander("View source documents"):
                    for source in sources:
                        st.caption(f"📄 {source}")
            st.caption(f"Generated by {model_name}")

            st.session_state[history_key].append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "model": model_name,
            })
        except Exception as exc:
            error_text = f"I couldn't complete that request: {exc}"
            st.error(error_text)
            st.session_state[history_key].append({
                "role": "assistant",
                "content": error_text,
            })


# -------------------------
# Sidebar navigation
# -------------------------
with st.sidebar:
    st.markdown("# 🤖 ABC")
    st.markdown("### Technologies")
    st.caption("ENTERPRISE INTELLIGENCE")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Overview", "Policy Assistant", "Order Calculator"],
    )

    st.divider()
    st.markdown("**PLATFORM**")
    st.caption("✦ Cloudflare Workers AI")
    st.caption("▦ Cloudflare D1 Database")
    st.caption("◇ Authenticated API Gateway")
    st.divider()
    st.caption("ABC Technologies")
    st.caption("Enterprise AI Demonstration")


# =========================================================
# PAGE 1 — OVERVIEW + HOMEPAGE AI CONCIERGE
# =========================================================
if page == "Overview":
    show_hero(
        "ENTERPRISE INTELLIGENCE PLATFORM",
        "Business operations, made smarter.",
        "A unified workspace for company knowledge, customer support and order calculations.",
    )

    st.markdown('<div class="section-kicker">SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
    st.subheader("Your AI operations at a glance")

    metric1, metric2, metric3 = st.columns(3, gap="medium")
    with metric1:
        st.metric("AI inference", "Workers AI", "GLM-4.7-Flash")
    with metric2:
        st.metric("Knowledge store", "Cloudflare D1", "3 policy records")
    with metric3:
        st.metric("API gateway", "Cloudflare", "Authenticated")

    st.write("")
    left, right = st.columns([1.3, 1], gap="large")

    with left:
        with st.container(border=True):
            st.markdown("### 👋 Welcome to ABC Technologies")
            st.write(
                "Explore company policies, get customer-aware answers, "
                "and calculate sample business orders through one workspace."
            )
            st.markdown(
                '<div class="soft-note"><b>Available workflows</b><br>'
                '📚 Company policy questions · 👤 Customer-aware responses · '
                '🧮 Validated order calculations</div>',
                unsafe_allow_html=True,
            )
            info1, info2 = st.columns(2)
            with info1:
                st.write("**📚 Policy Assistant**")
                st.caption("Ask about refunds, processing and support.")
            with info2:
                st.write("**🧮 Order Calculator**")
                st.caption("Calculate customer order totals.")

    with right:
        with st.container(border=True):
            st.markdown("### ☁️ Live service status")
            st.write("Check the deployed gateway and database connection.")
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

    # Homepage chatbot — visitors can interact without navigating away.
    st.write("")
    show_hero(
        "LIVE AI DEMONSTRATION",
        "Meet ABC AI Concierge.",
        "Ask a company-policy question and see the deployed AI assistant in action.",
    )

    with st.container(border=True):
        concierge_col, profile_col = st.columns([2, 1], gap="large")

        with profile_col:
            st.markdown("### 👤 Demo customer")
            home_customer = st.selectbox(
                "Choose a customer profile",
                ["customer_001", "customer_002"],
                format_func=customer_label,
                key="home_customer",
            )
            if home_customer == "customer_001":
                st.caption("Ahmed · Preferred currency: PKR · Contact: Email")
            else:
                st.caption("Sara · Preferred currency: USD · Contact: Email")

            st.markdown("**Try asking about:**")
            st.caption("• Refund deadlines")
            st.caption("• Order processing")
            st.caption("• Customer support hours")

            if st.button("Clear homepage conversation", key="clear_home_chat"):
                st.session_state[f"home_chat_{home_customer}"] = []
                st.rerun()

        with concierge_col:
            st.markdown("### 💬 Ask ABC AI")
            st.caption("Responses are generated using the deployed company knowledge base.")

            home_history_key = f"home_chat_{home_customer}"
            if home_history_key not in st.session_state:
                st.session_state[home_history_key] = []

            render_chat_history(st.session_state[home_history_key])

            # Clickable suggested prompts
            suggestion_columns = st.columns(3)
            suggested_questions = [
                "What is the refund deadline?",
                "How long does order processing take?",
                "When is customer support available?",
            ]
            selected_suggestion = None
            for index, suggestion in enumerate(suggested_questions):
                with suggestion_columns[index]:
                    if st.button(
                        ["↩ Refunds", "📦 Orders", "🎧 Support"][index],
                        key=f"home_suggestion_{index}",
                        use_container_width=True,
                    ):
                        selected_suggestion = suggestion

            home_prompt = st.chat_input(
                "Ask ABC AI about company policies...",
                key=f"home_chat_input_{home_customer}",
            )

            prompt_to_send = home_prompt or selected_suggestion
            if prompt_to_send:
                answer_policy_question(
                    home_customer,
                    prompt_to_send,
                    home_history_key,
                )

    st.caption(
        "Deployment: Streamlit Community Cloud · Cloudflare Workers · "
        "Workers AI · D1"
    )


# =========================================================
# PAGE 2 — POLICY ASSISTANT
# =========================================================
elif page == "Policy Assistant":
    show_hero(
        "CUSTOMER KNOWLEDGE",
        "Policy Assistant",
        "Ask questions about company policies and receive AI-generated responses grounded in company records.",
    )

    profile_col, chat_col = st.columns([1, 2.1], gap="large")

    with profile_col:
        with st.container(border=True):
            st.markdown("### 👤 Customer profile")
            policy_customer = st.selectbox(
                "Choose demo customer",
                ["customer_001", "customer_002"],
                format_func=customer_label,
                key="policy_customer",
            )

            if policy_customer == "customer_001":
                st.markdown("**Ahmed**")
                st.caption("Preferred currency: PKR")
                st.caption("Preferred contact: Email")
            else:
                st.markdown("**Sara**")
                st.caption("Preferred currency: USD")
                st.caption("Preferred contact: Email")

            st.divider()
            st.markdown("**Knowledge topics**")
            st.caption("📄 Customer Refund Policy")
            st.caption("📄 Order Processing Policy")
            st.caption("📄 Customer Support Guidelines")

            policy_history_key = f"policy_chat_{policy_customer}"
            if st.button("Clear this conversation", use_container_width=True):
                st.session_state[policy_history_key] = []
                st.rerun()

    with chat_col:
        with st.container(border=True):
            st.markdown("### 💬 Company knowledge assistant")
            st.caption("Ask a question below. Your conversation is retained for this active session.")

            if policy_history_key not in st.session_state:
                st.session_state[policy_history_key] = []

            render_chat_history(st.session_state[policy_history_key])

            policy_prompt = st.chat_input(
                "Ask about refunds, order processing or support...",
                key=f"policy_input_{policy_customer}",
            )

            if policy_prompt:
                answer_policy_question(
                    policy_customer,
                    policy_prompt,
                    policy_history_key,
                )


# =========================================================
# PAGE 3 — ORDER CALCULATOR
# =========================================================
elif page == "Order Calculator":
    show_hero(
        "BUSINESS OPERATIONS",
        "Order Calculator",
        "Prepare an order, validate the inputs and calculate the total through the live Cloudflare business API.",
    )

    input_col, result_col = st.columns([1.15, 1], gap="large")

    with input_col:
        with st.container(border=True):
            st.markdown("### 🧾 Order details")
            st.caption("Enter the customer and order information.")

            with st.form("order_calculator_form", border=False):
                order_customer = st.selectbox(
                    "Customer",
                    ["customer_001", "customer_002"],
                    format_func=customer_label,
                )

                default_price = 350.0 if order_customer == "customer_001" else 50.0
                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=100000,
                    value=8,
                    step=1,
                )
                unit_price = st.number_input(
                    "Unit price",
                    min_value=0.0,
                    max_value=1000000000.0,
                    value=default_price,
                    step=50.0 if order_customer == "customer_001" else 5.0,
                )

                submitted = st.form_submit_button(
                    "Calculate order total",
                    type="primary",
                    use_container_width=True,
                )

    with result_col:
        with st.container(border=True):
            st.markdown("### 📊 Calculation result")
            st.caption("Your verified order summary will appear here.")

            if submitted:
                try:
                    with st.spinner("Calculating order through Cloudflare..."):
                        result = call_assistant({
                            "customer_id": order_customer,
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


# -------------------------
# Footer
# -------------------------
st.divider()
st.caption(
    "ABC Technologies · Enterprise AI Demonstration · "
    "Streamlit + Cloudflare Workers AI + D1"
)
