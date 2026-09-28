
import streamlit as st
from agent import ask_agent

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Revenue Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f7f8fc;
    }

    /* Header */
    .main-header {
        padding: 1rem 0 0.5rem 0;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

  

    /* User message */
    .user-message {
        background: #eef2ff;
        padding: 12px 16px;
        border-radius: 14px;
        margin: 10px 0 10px auto;
        max-width: 80%;
        border: 1px solid #e0e7ff;
    }

    /* Assistant message */
    .assistant-message {
        background: #f9fafb;
        padding: 14px 16px;
        border-radius: 14px;
        margin: 10px auto 10px 0;
        max-width: 90%;
        border: 1px solid #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Sidebar button */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #374151;
        background: #1f2937;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: #374151;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.03);
    }

    .metric-number {
        font-size: 1.5rem;
        font-weight: 700;
    }

    .metric-label {
        color: #6b7280;
        font-size: 0.85rem;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.markdown("## 📊 Revenue AI")

    st.caption("AI-Powered Revenue Intelligence")

    st.divider()

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 💡 Example questions")

    examples = [
        "Why did profit decline from Q3 to Q4?",
        "Which region generated the most revenue in Q4?",
        "Which region had the biggest decline in profit?",
        "Which products have high return rates?",
        "Is delivery delay associated with returns?",
        "How much modeled opportunity is associated with discounting?"
    ]

    for example in examples:
        if st.button(example, key=example):
            st.session_state.pending_question = example
            st.rerun()

    st.divider()

    st.markdown("### 🔎 Analysis coverage")

    st.markdown("""
    **KPIs**
    - Revenue
    - Profit
    - Orders
    - Customers
    - AOV
    - Profit margin

    **Operational**
    - Returns
    - Delivery delays
    - Payment failures
    - Discounts

    **Commercial**
    - Marketing
    - ROAS
    - Financial opportunity

    **Statistics**
    - Chi-square
    - Statistical association
    """)

    st.divider()

    st.caption("Powered by Gemini + Python + Streamlit")


# -----------------------------
# Main header
# -----------------------------
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">📊 AI Revenue Intelligence</div>
        <div class="subtitle">
            Ask questions about revenue, profit, customers, operations and financial opportunities.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Top metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">₹13.8 Cr</div>
        <div class="metric-label">Total Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">4,312</div>
        <div class="metric-label">Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">2,580</div>
        <div class="metric-label">Customers</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">₹32.0L</div>
        <div class="metric-label">Conservative Modeled Opportunity</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)



# -----------------------------
# Chat history
# -----------------------------

if st.session_state.messages:

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="user-message">
                    <b>🧑 You</b><br><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="assistant-message">
                    <b>🤖 AI Analyst</b><br><br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)



# -----------------------------
# Handle example question
# -----------------------------
pending_question = st.session_state.pop("pending_question", None)


# -----------------------------
# Chat input
# -----------------------------
question = st.chat_input(
    "Ask a business question..."
)

if pending_question:
    question = pending_question


# -----------------------------
# Ask agent
# -----------------------------
if question:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate answer
    with st.spinner("🔎 Analyzing your business question..."):

        try:
            answer = ask_agent(question)

        except Exception as e:
            answer = f"⚠️ An error occurred: {str(e)}"

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Refresh page
    st.rerun()

