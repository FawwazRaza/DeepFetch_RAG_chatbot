import chromadb
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def diagnose_chroma_collection():
    try:
        chroma_client = chromadb.PersistentClient(path="./data_store")
        collection = chroma_client.get_or_create_collection(name="documents")
        
        print("chromadb collection diagnostics:")
        print(f"total documents in collection: {collection.count()}")
        
        try:
            results = collection.get(include=['embeddings', 'metadatas'])
            
            if not results or "embeddings" not in results or results["embeddings"] is None or len(results["embeddings"]) == 0:
                print("no embeddings found in chromadb")
                return

            embeddings = np.array(results["embeddings"])

            if embeddings.size > 0:
                print(f"found {len(embeddings)} embeddings")
            else:
                print("no valid embeddings found")

        except Exception as retrieve_error:
            print(f"retrieval error: {retrieve_error}")

        print("\nadditional diagnostics:")
        print(f"collection name: {collection.name}")

    except Exception as client_error:
        print(f"critical error: {client_error}")

def print_chroma_version():
    try:
        import chromadb
        print("\nchromadb version information:")
        print(f"chromadb version: {chromadb.__version__}")
    except Exception as e:
        print(f"error getting chromadb version: {e}")

if __name__ == "__main__":
    print("chromadb comprehensive diagnostic tool")
    print_chroma_version()
    diagnose_chroma_collection()
