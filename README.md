## DeepFetch RAG-Based AI Chatbot

This is a Retrieval-Augmented Generation (RAG)-based AI chatbot that combines document retrieval with generative AI to provide accurate and context-aware responses.

### Features
- **Document Processing**: Extracts text from PDFs, Word documents, and Markdown files.
- **Vector Storage**: Uses ChromaDB to store document embeddings.
- **Retrieval System**: Finds the most relevant document chunks for a query.
- **AI Response Generation**: Utilizes Mistral-7B to generate responses.
- **FastAPI Backend**: Provides an API for chatbot interactions.
- **Streamlit Frontend**: Offers a user-friendly interface.

### Setup Instructions
#### 1. Install Dependencies
Ensure Python 3.8+ is installed, then run:
```bash
pip install -r requirements.txt
```

#### 2. Download Models
##### Mistral-7B Model
```bash
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GGUF mistral-7b-instruct-v0.1.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
```
##### MiniLM Model
```bash
python download_model_minilm.py
```

#### 3. Process Documents
```bash
python document_processor.py
```

#### 4. Start Retrieval
```bash
python retrieval.py
```

#### 5. Authenticate Hugging Face
```python
from huggingface_hub import login
huggingface_token = "hf_xxxxxxxxxxxxxxxxxxxxxxx"
login(token=huggingface_token)
print("Successfully logged in to Hugging Face")
```

#### 6. Generate Responses
```bash
python response_generator.py
```

#### 7. Start Backend
```bash
uvicorn test_backend:app --host 0.0.0.0 --port 8000
```

#### 8. Run Frontend
```bash
streamlit run test_frontend.py
```

### Code Overview
- **document_processor.py**: Handles document ingestion and vector storage.
- **retrieval.py**: Searches for relevant document chunks.
- **response_generator.py**: Uses Mistral-7B to generate responses.
- **test_backend.py**: FastAPI backend exposing chatbot API.
- **test_frontend.py**: Streamlit frontend for user interaction.

### How It Works
1. **Document Processing**: Extracts text, chunks it, and stores embeddings in ChromaDB.
2. **Query Handling**: Retrieves the most relevant document chunks based on the user query.
3. **Response Generation**: Uses Mistral-7B to generate AI responses based on retrieved context.

---

