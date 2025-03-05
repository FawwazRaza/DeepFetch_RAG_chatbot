import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./data_store")
collection = chroma_client.get_or_create_collection(name="documents")


def search_documents(query, top_k=1):
    """Searches ChromaDB for the most relevant document chunks."""
    
    query_embedding = embedding_model.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # Ensure results["documents"] is a list before accessing
    if not results or "documents" not in results or not results["documents"]:
        return "⚠️ No relevant information found."

    retrieved_chunks = []
    for i in range(len(results["documents"][0])):
        try:
            metadata = results["metadatas"][0][i]  # Safely access metadata
            text_chunk = metadata.get("text", "No text available")
            source = metadata.get("source", "Unknown source")
            retrieved_chunks.append(f"📄 Source: {source}\n{text_chunk}\n")
        except (IndexError, KeyError) as e:
            print(f"Error processing metadata: {e}")

    return "\n---\n".join(retrieved_chunks) if retrieved_chunks else "⚠️ No relevant information found."


if __name__ == "__main__":

    while True:
        query = input("\n🔍 Enter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        response = search_documents(query)
        print("\n📢 Response:\n", response)
