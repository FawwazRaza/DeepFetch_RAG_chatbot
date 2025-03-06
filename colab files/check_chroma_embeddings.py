import chromadb
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def diagnose_chroma_collection():
    try:
        # Connect to ChromaDB
        chroma_client = chromadb.PersistentClient(path="./data_store")
        collection = chroma_client.get_or_create_collection(name="documents")
        
        # Print basic collection information
        print("🔍 ChromaDB Collection Diagnostics:")
        print(f"Total documents in collection: {collection.count()}")
        
        # Retrieve documents with correct include parameters
        # Retrieve documents with correct include parameters
        try:
            results = collection.get(include=['embeddings', 'metadatas'])
            
            # Ensure results exist and are not empty
            if not results or "embeddings" not in results or results["embeddings"] is None or len(results["embeddings"]) == 0:
                print("❌ No embeddings found in ChromaDB!")
                return



            embeddings = np.array(results["embeddings"])  # Convert to NumPy array safely

            if embeddings.size > 0:  # Proper check for non-empty array
                print(f"✅ Found {len(embeddings)} embeddings.")
            else:
                print("❌ No valid embeddings found.")

        except Exception as retrieve_error:
            print(f"❌ Retrieval Error: {retrieve_error}")


        # Additional collection metadata
        print("\n🛠️ Additional Diagnostics:")
        print(f"Collection Name: {collection.name}")

    except Exception as client_error:
        print(f"❌ Critical Error: {client_error}")

def print_chroma_version():
    try:
        import chromadb
        print("\n📦 ChromaDB Version Information:")
        print(f"ChromaDB Version: {chromadb.__version__}")
    except Exception as e:
        print(f"Error getting ChromaDB version: {e}")

if __name__ == "__main__":
    print("🔬 ChromaDB Comprehensive Diagnostic Tool 🔬")
    print_chroma_version()
    diagnose_chroma_collection()