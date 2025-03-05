import chromadb

# Define ChromaDB path
CHROMA_DB_PATH = "./data_store"

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

# Get stored documents
stored_data = collection.get()

# Print summary
print(f"🔍 Number of stored documents: {len(stored_data['documents'])}")

# Check metadata of stored documents
if stored_data["metadatas"]:
    print(f"✅ Example Metadata: {stored_data['metadatas'][:3]}")  # Show first 3
else:
    print("❌ No document metadata found in ChromaDB!")
