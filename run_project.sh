# chmod +x run_project.sh
# ./run_project.sh


#!/bin/bash

# Install dependencies
pip install -r requirements.txt

pip install transformers accelerate bitsandbytes sentencepiece
# Run and store chunk of data in the database
python download_model_minilm.py
python document_processor.py
python retrieval.py

# Download the Mistral-7B model from Hugging Face
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GGUF mistral-7b-instruct-v0.1.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False

# Run the response generator
python response_generator.py &

# Start the FastAPI backend in a new terminal
gnome-terminal -- bash -c "uvicorn backend:app --host 0.0.0.0 --port 8000 --reload; exec bash" &

# Wait a few seconds to ensure the API starts properly
sleep 5

echo "Your API is now running at: http://127.0.0.1:8000/docs 🎉"

# Start the Streamlit frontend in another terminal
gnome-terminal -- bash -c "streamlit run frontend.py; exec bash" &
