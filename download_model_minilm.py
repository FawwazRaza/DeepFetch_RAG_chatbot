from sentence_transformers import SentenceTransformer

# Specify a local cache folder
model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./models")

print("Model downloaded successfully!")
