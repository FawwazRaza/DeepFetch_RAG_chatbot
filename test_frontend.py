import streamlit as st
import requests

with open("backend_url.txt", "r") as f:
    API_URL = f.read().strip()

st.title("AI chatbot")

user_id = "test_user"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def chat_with_bot(query):
    """Fetches response from FastAPI chatbot."""
    try:
        response = requests.get(API_URL, params={"q": query})
        if response.status_code == 200:
            return response.json()["response"]
        return "error: could not fetch response."
    except requests.exceptions.ConnectionError:
        return "error: backend server is unreachable. please check if FastAPI is running."

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

query = st.chat_input("Ask a question...")
if query:
    st.session_state.chat_history.append({"role": "user", "text": query})
    with st.chat_message("user"):
        st.markdown(query)

    reply = chat_with_bot(query)
    st.session_state.chat_history.append({"role": "assistant", "text": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
