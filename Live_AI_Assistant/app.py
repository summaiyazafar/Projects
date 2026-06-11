import streamlit as st
from assistant import get_live_assistant
from langchain_core.messages import HumanMessage, AIMessage

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Live AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# TOP BAR UI (CHATGPT STYLE)
# -------------------------
# -------------------------
# TOP BAR UI (FIXED)
# -------------------------
top_left, top_center, top_right = st.columns([2, 6, 2])

with top_center:
    st.markdown(
    """
    <div style="text-align:center; line-height:1.2;">
        <h2 style="margin:0;">🤖 Live AI Assistant</h2>
        <p style="margin:0; font-size:14px; color:gray;">
            AI + Web Search + Memory System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

with top_right:
    st.markdown("##### 🚀 Share | 🎁 Offer")

st.divider()

# -------------------------
# INIT AGENT
# -------------------------
if "agent" not in st.session_state:
    st.session_state.agent = get_live_assistant()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I am your Live AI Assistant. Ask me anything!"
        }
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# SIDEBAR (CONTROL PANEL)
# -------------------------
with st.sidebar:
    st.title("🧠 Control Panel")

    mode = st.radio(
        "Mode",
        ["💬 Chat", "🔍 Web Search"]
    )

    st.markdown("---")

    if st.button(" New Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    st.write("📜 Recent Chats")

    for msg in st.session_state.messages[-10:]:
        st.write(f"• {msg['role']}: {msg['content'][:30]}...")

    st.markdown("---")

    st.markdown("##### 👤 Account")

    if st.button("🆕 Sign Up"):
        st.success("Signup feature coming soon 🚀")

# -------------------------
# SHOW CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_query = st.chat_input("Ask anything...")

# -------------------------
# MAIN LOGIC
# -------------------------
if user_query:

    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(f"🧑 {user_query}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking + Searching Web... 🌐"):

            try:
                messages = (
                    st.session_state.chat_history
                    + [HumanMessage(content=user_query)]
                )

                response = st.session_state.agent.invoke(
                    {"messages": messages}
                )

                if isinstance(response, dict) and "messages" in response:
                    last_message = response["messages"][-1]
                    output_text = getattr(last_message, "content", str(last_message))
                else:
                    output_text = str(response)

                st.markdown(f"🤖 {output_text}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output_text
                })

                st.session_state.chat_history.append(
                    HumanMessage(content=user_query)
                )

                st.session_state.chat_history.append(
                    AIMessage(content=output_text)
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")