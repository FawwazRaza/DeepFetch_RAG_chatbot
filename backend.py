from fastapi import FastAPI, Query
from llama_cpp import Llama
from retrieval import search_documents

# Load the model
MODEL_PATH = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=4096)

app = FastAPI()

# Store chat history for each user
chat_history = {}

def generate_response(user_id: str, query: str):
    """Generates a response while maintaining conversation history."""
    
    # Retrieve relevant documents
    context = search_documents(query, top_k=3)
    if not context or "⚠️ No relevant information found." in context:
        return "❌ Sorry, I couldn't find relevant information."

    # Append chat history
    history = chat_history.get(user_id, [])
    history.append(f"User: {query}")
    
    prompt = f"""
    You are an AI assistant using retrieved knowledge to answer queries. 
    Use the following context:
    
    {context}

    Chat history:
    {' '.join(history)}

    User: {query}
    AI:
    """

    # Generate response
    response = llm(prompt, max_tokens=256, temperature=0.7, stop=["\n\n"])
    reply = response["choices"][0]["text"].strip()

    # Save response to history
    history.append(f"AI: {reply}")
    chat_history[user_id] = history[-5:]  # Keep last 5 messages
    
    return reply

@app.get("/query/")
def query_chatbot(user_id: str, q: str = Query(..., description="User's query")):
    return {"response": generate_response(user_id, q)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
