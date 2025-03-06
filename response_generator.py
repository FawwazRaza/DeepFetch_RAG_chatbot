import os
from llama_cpp import Llama
from retrieval import search_documents

# Load the LLM model (Ensure the model file is present)
MODEL_PATH = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"  # Update with actual path

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("⚠️ Download the Mistral-7B model in GGUF format first!")

# Load Mistral with a context window of 4096 tokens
llm = Llama(model_path=MODEL_PATH, n_ctx=4096)

def generate_response(query):
    """Generates a response using retrieved documents as context."""
    
    # Retrieve relevant document chunks
    context = search_documents(query, top_k=3)

    if not context or "⚠️ No relevant information found." in context:
        return "❌ Sorry, I couldn't find relevant information."

    # Format the prompt for LLM
    prompt = f"""
    You are a helpful AI assistant answering user queries based on provided documents.
    Use the following context to generate a relevant response and if the reponse is not relevant, please let the user know that you couldn't find relevant information.:

    {context}

    User question: {query}
    Answer:
    """

    try:
        # Run inference on LLM
        response = llm(
            prompt=prompt,
            max_tokens=100,
            temperature=0.1,
            stop=["\n\n"]
        )
        
        return response["choices"][0]["text"].strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


if __name__ == "__main__":
    while True:
        query = input("\n💬 Ask a question (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        response = generate_response(query)
        print("\n🤖 AI Response:\n", response)
