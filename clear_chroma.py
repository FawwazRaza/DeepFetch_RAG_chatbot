# import chromadb

# # Define ChromaDB path
# CHROMA_DB_PATH = "./data_store"

# # Connect to ChromaDB
# chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
# collection = chroma_client.get_or_create_collection(name="documents")

# # Delete all existing data
# all_ids = collection.get()["ids"]  # Get all stored IDs
# if all_ids:
#     collection.delete(ids=all_ids)
#     print(f"✅ Deleted {len(all_ids)} documents from ChromaDB.")
# else:
#     print("⚠️ No documents found to delete.")

# print("✅ ChromaDB cleared. Reprocessing documents...")
import shutil
import os

# Clear existing data store
shutil.rmtree('./data_store', ignore_errors=True)
os.makedirs('./data_store')