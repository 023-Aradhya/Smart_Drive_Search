import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Google Drive AI Agent",
    layout="centered"
)

st.title("📁 Google Drive AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask about your files...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    try:
        response = requests.post(
            API_URL,
            json={"message": user_input}
        )
        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get(
                "response",
                "No response received."
            )
        else:
            bot_reply = f"Error: {response.status_code}"

    except Exception as e:
        bot_reply = f"Exception occurred: {str(e)}"

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)