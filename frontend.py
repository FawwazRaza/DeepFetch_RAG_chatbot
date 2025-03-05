import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query/"

st.title("💬 AI Chatbot")

user_id = "test_user"  # Can be dynamic for different users
chat_history = []

def chat_with_bot(query):
    response = requests.get(API_URL, params={"user_id": user_id, "q": query})
    if response.status_code == 200:
        return response.json()["response"]
    return "❌ Error: Could not fetch response."

# Chat UI
query = st.text_input("Ask a question:")
if st.button("Send"):
    if query:
        reply = chat_with_bot(query)
        chat_history.append(f"**You:** {query}")
        chat_history.append(f"**Bot:** {reply}")
        st.write("\n".join(chat_history))
