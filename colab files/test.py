import os
import chromadb
from llama_cpp import Llama
from retrieval import search_documents
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./data_store")
collection = chroma_client.get_or_create_collection(name="documents")

# Load Mistral LLM Model
MODEL_PATH = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("⚠️ Download the Mistral-7B model in GGUF format first!")

# Load Llama with a timeout to avoid infinite wait
llm = Llama(model_path=MODEL_PATH, n_ctx=4096)

def generate_response(query):
    """Generate AI response using retrieved documents as context."""

    # Retrieve relevant documents
    context = search_documents(query, top_k=3)

    # If no relevant documents are found, return "I don't know"
    if not context or "⚠️ No relevant information found." in context:
        return "🤖 I don't know. The answer is not in my dataset."

    # **Check if retrieved content is relevant to the query**
    keywords = query.lower().split()  # Break question into words
    relevant = any(word in context.lower() for word in keywords)  # Check for matching words

    if not relevant:
        return "🤖 I don't know. The answer is not in my dataset."

    # Format the prompt for Llama
    prompt = f"""
    You are a helpful AI assistant. Answer only if the context contains relevant information.
    If the answer is not in the context, respond with: "I don't know. The answer is not in my dataset."

    Context:
    {context}

    User question: {query}
    Answer:
    """

    print("\n📝 Prompt Sent to Llama:\n", prompt)  # Debugging output

    try:
        # Generate response using Llama
        response = llm.create_completion(
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
            stop=["\n\n"]
        )

        answer = response["choices"][0]["text"].strip()

        # If the model response is empty, return "I don't know."
        if not answer:
            return "🤖 I don't know. The answer is not in my dataset."

        return answer

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

if __name__ == "__main__":
    import threading

    def chat_loop():
        while True:
            try:
                query = input("\n💬 Ask a question (or type 'exit' to quit): ").strip()
                
                if query.lower() == "exit":
                    print("Chatbot stopped.")
                    break
                
                # Run response generation in a separate thread to avoid getting stuck
                response_thread = threading.Thread(target=lambda: print("\n🤖 AI Response:\n", generate_response(query)))
                response_thread.start()
                response_thread.join(timeout=30)  # Timeout to prevent infinite freezing
                
                if response_thread.is_alive():
                    print("⚠️ Response took too long. Restarting chatbot...")

            except KeyboardInterrupt:
                print("\n⚠️ Chatbot interrupted. Exiting.")
                break

    chat_loop()
