import torch
import chromadb
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from retrieval import search_documents

login(token="hf_......")

model_name = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)

if tokenizer.eos_token is None:
    tokenizer.add_special_tokens({'eos_token': '<|endoftext|>'})

tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto",
    token=True
).to("cuda")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="./data_store")
collection = chroma_client.get_or_create_collection(name="documents")

def select_best_context(query, retrieved_chunks):
    if not retrieved_chunks:
        print("no relevant data found")
        return None
    
    print(f"processing query: {query}")
    query_embedding = embedding_model.encode(query)
    best_score = -1
    best_context = None
    
    for chunk in retrieved_chunks:
        chunk_embedding = embedding_model.encode(chunk)
        similarity = torch.nn.functional.cosine_similarity(
            torch.tensor(query_embedding), 
            torch.tensor(chunk_embedding), 
            dim=0
        ).item()

        if similarity > best_score:
            best_score = similarity
            best_context = chunk
    
    print(f"best similarity score: {best_score:.4f}")
    return best_context

def generate_response(prompt, context, max_length=512):
    if context is None:
        return "no relevant data found"

    full_prompt = f"[INST] context: {context}\n\nuser: {prompt}\nassistant: [/INST]"
    print("generating response...")

    inputs = tokenizer(
        full_prompt, return_tensors="pt", padding=True, truncation=True, max_length=max_length
    ).to("cuda")

    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=max_length,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.strip()

if __name__ == "__main__":
    print("chatbot is running. type 'exit' to quit.")
    while True:
        query = input("you: ")
        if query.lower() == "exit":
            print("exiting chatbot. goodbye!")
            break
        
        retrieved_chunks = search_documents(query, top_k=3)
        print("retrieving relevant data...")
        
        best_context = select_best_context(query, retrieved_chunks)
        response = generate_response(query, context=best_context)
        
        print("ai response:")
        print(response)
