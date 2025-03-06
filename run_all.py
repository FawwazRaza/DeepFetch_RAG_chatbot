import subprocess

files = ["download_model_minilm.py", "document_processor.py", "retrieval.py","response_generator.py"]

for file in files:
    subprocess.run(["python", file])
