import streamlit as st
import requests

# FastAPI Server URL
API_URL = "http://127.0.0.1:8000/query/"

# Streamlit App Title
st.title("💬 AI Chatbot")

# Unique User ID (Can be made dynamic per session)
user_id = "test_user"

# Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_bot(query):
    """Fetches response from FastAPI chatbot."""
    try:
        response = requests.get(API_URL, params={"user_id": user_id, "q": query})
        if response.status_code == 200:
            return response.json()["response"]
        return "❌ Error: Could not fetch response."
    except requests.exceptions.ConnectionError:
        return "⚠️ Error: Backend server is unreachable. Please check if FastAPI is running."

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# User Input Box
query = st.chat_input("Ask a question...")
if query:
    # Display user message
    st.session_state.chat_history.append({"role": "user", "text": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Get AI response
    reply = chat_with_bot(query)
    st.session_state.chat_history.append({"role": "assistant", "text": reply})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(reply)
