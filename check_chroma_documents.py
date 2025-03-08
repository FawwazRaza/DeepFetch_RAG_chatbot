import chromadb

CHROMA_DB_PATH = "./data_store"

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(name="documents")

stored_data = collection.get()

print(f"Number of stored documents: {len(stored_data['documents'])}")

if stored_data["metadatas"]:
    print(f"Example metadata: {stored_data['metadatas'][:3]}") 
else:
    print("No document metadata found in ChromaDB!")
